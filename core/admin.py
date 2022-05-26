"""Define them admins."""
from django.contrib import admin

from core import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass
