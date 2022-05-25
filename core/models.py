"""Defines them models."""
from django.db import models


class Recipe(models.Model):
    """Defines a recipe."""

    title = models.TextField()
    url = models.URLField()
    html = models.TextField()
    source = models.CharField(max_length=255)

    @classmethod
    def from_recipe_page(cls, recipe_page: "core.recipes.RecipePage") -> "Recipe":
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
            "html": self.html,
            "source": self.source,
        }
