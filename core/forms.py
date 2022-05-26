"""Forms."""

from django import forms


class SearchForm(forms.Form):
    """The search form."""

    query = forms.CharField(label="Search", max_length=100)
