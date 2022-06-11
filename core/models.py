"""Defines them models."""
from typing import TYPE_CHECKING

from django.db import models

if TYPE_CHECKING:
    from core.recipes import RecipePage


class Recipe(models.Model):
    """Defines a recipe."""
    id: models.IntegerField
    title: models.TextField = models.TextField()
    url: models.URLField = models.URLField()
    html: models.TextField = models.TextField()
    source: models.CharField = models.CharField(max_length=255)

    @classmethod
    def from_recipe_page(cls, recipe_page: "RecipePage") -> "Recipe":
        """Instantiate a recipe from the recipe page instance."""
        return cls(
            title=recipe_page.title,
            url=recipe_page.url,
            html=recipe_page.html,
            source="Recipes Wiki",
        )

    @property
    def to_es_document(self) -> dict:
        """Generate an elasticsearch document from this model."""
        return {
            "_op_type": "index",
            "_index": "recipes",
            "_id": self.id,
            "title": self.title,
            "url": self.url,
            "recipe": self.html,
            "source": self.source,
        }

    def __str__(self):
        """Cast to string."""
        return f"{self.title} ({self.id})"
