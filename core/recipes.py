"""Tooling for recipes."""

import functools
import json
import logging
from typing import List, Optional

import requests
from boltons.iterutils import first, get_path
from bs4 import BeautifulSoup
from django.conf import settings
from elasticsearch import helpers
from kafka import KafkaConsumer, KafkaProducer

from core.es import get_es_client
from core import models

RECIPE_MAPPING = {
    "recipe_id": {"type": "integer"},
    "recipe": {
        "type": "text",
        "analyzer": "text_strip_html",
        "position_increment_gap": 100,
        "copy_to": "text",
        "search_analyzer": "text_strip_html",
    },
    "source": {"type": "keyword"},
    "title": {"type": "text"},
    "text": {
        "type": "text",
        "analyzer": "text_strip_html",
        "position_increment_gap": 100,
        "search_analyzer": "text_strip_html",
    },  # a catch-all
    "url": {"type": "keyword"},
}


class RecipePage:
    """Encapsulates a recipe page."""

    def __init__(self, data):
        """Initialize the class."""
        self._data = data
        self._wikitext = None

    @property
    def url(self) -> str:
        """Return the URL of the page."""
        return self._data["url"]

    @property
    def title(self) -> str:
        """Return page title."""
        return self._data["title"]

    @functools.cached_property
    def html(self) -> bytes:
        """Retrieve HTML from page."""
        resp = requests.get(f"https://recipes.fandom.com{self.url}")
        return resp.content

    @functools.cached_property
    def inner_html(self) -> str:
        """Retrieve inner HTML."""
        inner = first(
            BeautifulSoup(self.html, "html.parser").html.find_all(
                "div", {"class": "mw-parser-output"}
            )
        )
        if inner:
            return inner.decode()
        return ""

    def to_json_message(self, include_html=False) -> dict:
        """Generate a message for Kafka."""
        dct = {"title": self.title, "url": self.url}
        if include_html:
            dct["html"] = self.inner_html
        return dct


class RecipePageGenerator:
    """Allows us to iterate on recipe pages."""

    def __init__(self, offset=None, **_kwargs):
        """Initialize the class."""
        self.pages = []
        self.offset = offset
        self.end_of_list = False

    def __iter__(self):
        """Mark as an iterator."""
        return self

    def __next__(self):
        """Ensure compatibility."""
        return self.next()

    def next(self) -> RecipePage:
        """Return a page, lazily loading more when necessary."""
        if self.pages == []:
            if self.end_of_list:
                raise StopIteration()
            result = requests.get(
                "https://recipes.fandom.com/api/v1/Articles/List",
                params={"offset": self.offset},
            ).json()
            self.pages = result["items"]
            self.pages.reverse()
            if "offset" in result:
                self.offset = result["offset"]
            else:
                self.end_of_list = True
        return RecipePage(self.pages.pop())


def run_recipe_producer(*_args, **kwargs):
    """Run the producer for recipe indexing."""
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_BROKERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    for page in RecipePageGenerator(**kwargs):
        json_message = page.to_json_message()
        logging.debug("Sending message %s", json_message)
        producer.send("recipes", json_message)


def handle_recipe(recipe_json_string: str) -> Optional[models.Recipe]:
    """Handle a recipe by getting / creating model instances and yielding es doc."""
    try:
        recipe_json = json.loads(recipe_json_string)
        recipe_page = RecipePage(recipe_json)
        recipe = models.Recipe.objects.filter(url=recipe_page.url).first()
        if not recipe:
            recipe = models.Recipe.from_recipe_page(recipe_page)
        recipe.title = recipe_page.title
        recipe.url = recipe_page.url
        recipe.html = recipe_page.inner_html
        recipe.source = "Recipes Wiki"
        recipe.save()
        return recipe
    except json.JSONDecodeError as json_error:
        logging.error("Could not decode: %s", json_error)
    except Exception as exc:  # pylint: disable=broad-except
        logging.error("Unhandled exception: %s", exc)
    return None


def yield_recipe_messages():
    """Yields a dict for generating the appropriate doc"""
    for consumer_message in KafkaConsumer(
        "recipes",
        group_id="recipe_consumer",
        bootstrap_servers=settings.KAFKA_BROKERS,
    ):
        recipe = handle_recipe(consumer_message.value)
        if recipe:
            try:
                es_document = recipe.to_es_document
                logging.warning("Yielding ES document: %s", es_document)
                yield es_document
            except Exception as exc:  # pylint: disable=broad-except
                logging.error("Unhandled exception: %s", exc)


def run_recipe_consumer():
    """Run the consumer, wrapped in an ES context."""
    for okay, result in helpers.streaming_bulk(
        get_es_client(),
        yield_recipe_messages(),
        chunk_size=50,
    ):
        logging.debug(okay)
        logging.debug(result)


def find_recipes(query, size=20):
    """Find recipes."""
    return get_es_client().search(
        index="recipes", query={"match": {"text": query}}, size=size
    )


class RecipeHit:
    """A recipe hit."""

    def __init__(self, hit):
        """Initialize the class."""
        self.hit = hit

    @property
    def title(self) -> str:
        """Return title."""
        return self.hit["_source"]["title"]

    @property
    def recipe(self) -> str:
        """Return recipe."""
        return self.hit["_source"]["recipe"]

    @classmethod
    def many_from_result(cls, search_result) -> List["RecipeHit"]:
        """Return a list of recipes from a search result."""
        return [cls(x) for x in get_path(search_result, ("hits", "hits"), [])]
