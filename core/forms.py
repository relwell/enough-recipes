"""Forms."""

from django import forms


class SearchForm(forms.Form):
    """The search form."""

    query = forms.CharField(label="", max_length=100)
