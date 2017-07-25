"""View page for our homeless to hearth app."""
from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render
from search.models import Resource


class HomePageView(TemplateView):
    """Class home page view."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """."""
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context


class SearchView(ListView):
    """Class based search view."""

    template_name = "search.html"
    model = Resource

    def get_queryset(self):
        try:
            o_name = self.kwargs['org_name']
        except:
            o_name = ''
        if (o_name != ''):
            object_list = self.model.objects.filter(self.model.objects.org_name)
        else:
            object_list = self.model.objects.all()
        return object_list
