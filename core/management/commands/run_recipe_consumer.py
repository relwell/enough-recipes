"""Pull recipes from recipe wiki."""
from django.core.management.base import BaseCommand

from recipes import run_recipe_consumer


class Command(BaseCommand):
    """Does the command."""

    help = "Pull recipes from the recipe wiki."

    def handle(self, *_args, **_options):
        """Consume recipe messages from Kafka for indexing."""
        run_recipe_consumer()
