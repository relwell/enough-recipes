from django.shortcuts import render

from boltons.iterutils import get_path

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
    hits = [RecipeHit(x) for x in get_path(search_result, ("hits", "hits"), [])]
    return render(
        request,
        "core/search.html",
        {"form": form, "query": query, "hits": hits},
    )
