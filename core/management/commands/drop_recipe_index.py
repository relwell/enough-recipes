"""Creates the recipe index."""
import logging

from django.core.management.base import BaseCommand

from core.es import drop_index, get_es_client
from core.recipes import RECIPE_MAPPING


class Command(BaseCommand):
    """Does the command."""

    help = "Create the recipe index on elasticsearch."

    def handle(self, *_args, **_options):
        """Create the recipe index on elasticsearch."""
        drop_index(get_es_client(), "recipes")
