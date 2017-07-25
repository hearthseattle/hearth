"""View page for our homeless to hearth app."""
from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile
from django.views.generic.base import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    """Class home page view."""

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        """."""
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context
