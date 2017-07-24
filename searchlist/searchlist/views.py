"""View page for our homeless to hearth app."""
from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile
from django.views.generic.base import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    def get(self, request):
        return render(request, 'home.html')

# class SearchView(generic.ListView):
#     template_name = 
#     page_template = 
#     context_object_name = 
#     model = 

#     def get_context_data(self, **kwargs):
#         context = super(SearchView, self).get_context_data(**kwargs)
#         context.update({
#             ''
#         })