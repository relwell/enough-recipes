"""Pull recipes from recipe wiki."""
import logging

from django.core.management.base import BaseCommand

from core.recipes import run_recipe_consumer


class Command(BaseCommand):
    """Does the command."""

    help = "Pull recipes from the recipe wiki."

    def handle(self, *_args, **_options):
        """Consume recipe messages from Kafka for indexing."""
        logging.basicConfig(level="DEBUG")
        logging.info("Starting consumer...")
        run_recipe_consumer()
