import logging

from django.conf import settings
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError


def get_es_client() -> Elasticsearch:
    """Retrieve an elasticsearch client from env configs."""
    hosts = settings.ES_HOSTS
    hosts = hosts.split(",") if hosts else None

    # we could use IAM-based auth
    # https://elasticsearch-py.readthedocs.io/en/master/index.html#running-on-aws-with-iam
    return Elasticsearch(hosts=hosts)


def create_index(client, index=None, doc_type=None, mapping=None, **kwargs):
    """Initialize mappings for the product index."""
    es_settings = {
        # just one shard for now, no replicas for testing
        "number_of_shards": kwargs.get("num_shards", 1),
        "number_of_replicas": kwargs.get("num_replicas", 0),
    }
    if "synonyms" in kwargs:
        es_settings["analysis"] = {
            "normalizer": {
                "keyword_lowercase": {"type": "custom", "filter": ["lowercase"]}
            },
            "filter": {
                "synonym_filter": {"type": "synonym", "synonyms": kwargs["synonyms"]}
            },
            "analyzer": {
                "text_strip_html": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "char_filter": ["html_strip"],
                    "filter": ["lowercase", "synonym_filter", "snowball"],
                }
            },
        }
    create_index_body = {
        "settings": es_settings,
        "mappings": {doc_type: {"properties": mapping}},
    }

    # create empty index
    try:
        client.indices.create(index=index, body=create_index_body)
        client.indices.put_mapping(
            index=index, doc_type=doc_type, body={"properties": mapping}
        )
        client.indices.open(index=index)
    except TransportError as e:
        logging.warning("Error working with index: %s", e)
        # ignore already existing index
        if e.error == "index_already_exists_exception":
            pass
        else:
            raise
