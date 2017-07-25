"""View page for our homeless to hearth app."""
from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render
# from search.models import SearchProfile
import operator
from django.db.models import Q


class HomePageView(TemplateView):
    """Class home page view."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """."""
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context


class SearchFormView(ListView):
    """Display a Resource list filtered by a search query."""

    def get_queryset(self):
        """Get a query for our search."""
        result = super(SearchFormView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(tags__icontains=q) for q in query_list)) | 
                reduce(operator.and_,
                       (Q(tags__icontains=q) for q in query_list))
            )
        return result