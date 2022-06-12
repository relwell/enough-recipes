"""Django views."""
from django.shortcuts import render

from core.forms import SearchForm
from core.recipes import find_recipes, scroll_recipes, RecipeHit


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
        {
            "form": form,
            "query": query,
            "hits": hits,
            "scroll_id": search_result["_scroll_id"],
        },
    )


def search_ajax(request):
    """Perform ajax search request."""
    scroll_id = request.GET["scroll_id"]
    search_result = scroll_recipes(scroll_id)
    print(search_result)
    hits = RecipeHit.many_from_result(search_result)
    return render(
        request,
        "core/search_results.html",
        {
            "hits": hits,
            "scroll_id": search_result["_scroll_id"],
        },
    )
