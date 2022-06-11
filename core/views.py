"""Django views."""
from django.shortcuts import render

from core.forms import SearchForm
from core.recipes import find_recipes, RecipeHit


def index(request):
    """Index view."""
    return render(request, "core/index.html", {"form": SearchForm()})


def search(request):
    """Search view."""
    form = SearchForm(request.GET)
    query = form["query"].value()
    search_result = find_recipes(query)
    hits = RecipeHit.many_from_result(search_result)
    return render(
        request,
        "core/search.html",
        {"form": form, "query": query, "hits": hits},
    )
