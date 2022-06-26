"""Provides tests for the app."""
from unittest.mock import patch, MagicMock

from django.test import TestCase

from core.recipes import find_recipes


class TestSearch(TestCase):
    """Tests search functionality."""

    @patch("core.es.get_es_client")
    def test_find_recipes_searches_query(self, get_es_client):
        """Assert that we use the right search params for our core recipe search."""
        es_client = MagicMock()
        get_es_client.return_value = es_client
        find_recipes("tofu")
        es_client.search.assert_called_with(
            index="recipes", query={"match": {"text": "tofu"}}, size=20, scroll="10m"
        )
