"""Tooling for recipes."""

import functools
import json
import logging
from typing import Optional

import requests
from elasticsearch import helpers
from kafka import KafkaConsumer, KafkaProducer
from core.es import get_es_client
from core import models

RECIPE_MAPPING = {
    "recipe_id": {"type": "number"},
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
        return f"https://recipes.fandom.com/{self._data['url']}"

    @property
    def title(self) -> str:
        """Return the title of the page without the wiki prefix."""
        return self._data["url"].replace("/wiki/", "")

    @functools.cached_property
    def html(self) -> str:
        """Retrieve HTMl from visual editor."""
        resp = requests.get(
            f"https://recipes.fandom.com/api.php?action=visualeditor&format=json&paction=parse&page={self.title}&uselang=en&formatversion=2"
        ).json()
        return resp["visualeditor"]["content"]

    @property
    def to_json_message(self, include_html=False) -> dict:
        """Generate a message for Kafka."""
        dct = {"title": self.title, "url": self.url}
        if include_html:
            dct["html"] = self.html
        return dct


class RecipePageGenerator:
    """Allows us to iterate on recipe pages."""

    def __init__(self, offset=None):
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


def run_recipe_producer():
    """Run the producer for recipe indexing."""
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode("utf-8"))
    for page in RecipePageGenerator():
        producer.send("recipes", page.to_json_message)


def handle_recipe(recipe_json_string: str) -> Optional[models.Recipe]:
    """Handle a recipe by getting / creating model instances and yielding es doc."""
    try:
        recipe_json = json.loads(recipe_json_string)
        recipe_page = RecipePage(recipe_json)
        recipe = Recipe.objects.filter(url=recipe_page.url).first()
        if not recipe:
            recipe = Recipe.from_recipe_page(recipe_page)
        recipe.title = recipe_page.title
        recipe.url = recipe_page.url
        recipe.html = recipe_page.html
        recipe.source = "Recipes Wiki"
        recipe.save()
        return recipe
    except json.JSONDecodeError as json_error:
        logging.error("Could not decode: %s", json_error)
    return None


def yield_recipe_messages():
    """Yields a dict for generating the appropriate doc"""
    for recipe_json in KafkaConsumer("recipes"):
        recipe = handle_recipe(recipe_json)
        if recipe:
            yield recipe.to_es_document


def run_recipe_consumer():
    """Run the consumer."""
    for okay, result in helpers.streaming_bulk(
        get_es_client(),
        yield_recipe_messages,
        chunk_size=50,
    ):
        logging.debug(okay)
        logging.debug(result)
