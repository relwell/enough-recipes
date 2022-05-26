"""Pull recipes from recipe wiki."""
from django.core.management.base import BaseCommand

from core.recipes import run_recipe_producer


class Command(BaseCommand):
    """Does the command."""

    help = "Pull recipes from the recipe wiki."

    def add_arguments(self, parser):
        """Add arguments."""
        parser.add_argument("--offset", type=str)

    def handle(self, *_args, **kwargs):
        """Produce recipes."""
        run_recipe_producer(**kwargs)
