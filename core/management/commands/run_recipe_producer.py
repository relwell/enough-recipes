"""Pull recipes from recipe wiki."""
from django.core.management.base import BaseCommand

from core.recipes import run_recipe_producer


class Command(BaseCommand):
    """Does the command."""

    help = "Pull recipes from the recipe wiki."

    def handle(self, *_args, **_options):
        """Produce recipes."""
        # todo: add ability to resume from latest instance in the DB
        run_recipe_producer()
