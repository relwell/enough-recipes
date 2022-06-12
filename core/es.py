"""Elasticsearch helpers."""
import logging

from typing import List

from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError


def get_es_hosts() -> List[str]:
    """Retrieve an optional list of hosts."""
    hosts = getattr(settings, "ES_HOSTS", "")
    return hosts.split(",")


def get_es_client() -> Elasticsearch:
    """Retrieve an elasticsearch client from env configs."""
    return Elasticsearch(hosts=list(get_es_hosts()))


def create_index(client, index=None, mapping=None, **kwargs):
    """Initialize mappings for the product index."""
    es_settings = {
        # just one shard for now, no replicas for testing
        "number_of_shards": kwargs.get("num_shards", 1),
        "number_of_replicas": kwargs.get("num_replicas", 0),
    }
    es_settings["analysis"] = {
        "normalizer": {
            "keyword_lowercase": {"type": "custom", "filter": ["lowercase"]}
        },
        "analyzer": {
            "text_strip_html": {
                "type": "custom",
                "tokenizer": "standard",
                "char_filter": ["html_strip"],
                "filter": ["lowercase", "snowball"],
            }
        },
    }
    create_index_body = {
        "settings": es_settings,
        "mappings": {"properties": mapping},
    }

    # create empty index
    try:
        client.indices.create(index=index, body=create_index_body)
        client.indices.put_mapping(index=index, body={"properties": mapping})
        client.indices.open(index=index)
    except TransportError as exc:
        logging.warning("Error working with index: %s", exc)
        # ignore already existing index
        if "index_already_exists_exception" in exc.errors:
            pass
        else:
            raise


def drop_index(client, index_name):
    """Drop the products index."""
    logging.warning("Dropping product index %s...", index_name)
    client.indices.delete(index=index_name, ignore=[404])
    logging.info("...done")
