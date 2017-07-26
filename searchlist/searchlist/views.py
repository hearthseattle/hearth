"""View page for our homeless to hearth app."""
from __future__ import unicode_literals
from django.core.files.storage import default_storage
from django.db.models.fields.files import FieldFile
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.shortcuts import render
import operator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from searchlist.models import Resource


class CreateResource(LoginRequiredMixin, CreateView):
    """Class-based view to create new resources."""

    template_name = 'searchlist/resource_form.html'
    model = Resource
    fields = ['main_category', 'ratings', 'age_range', 'org_name',
              'description', 'street', 'city', 'state', 'zip_code', 'website',
              'phone_number', 'tags']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Save form if valid."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(CreateResource, self).form_valid(form)


class EditResource(LoginRequiredMixin, UpdateView):
    """Class-based view to edit resources."""

    template_name = 'searchlist/resource_form.html'
    model = Resource
    fields = ['main_category', 'ratings', 'age_range', 'org_name',
              'description', 'street', 'city', 'state', 'zip_code', 'website',
              'phone_number', 'tags']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Save form if valid."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(EditResource, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """."""
        context = super(EditResource, self).get_context_data(**kwargs)
        context["edit"] = True
        return context


class DeleteResource(LoginRequiredMixin, DeleteView):
    """Class-based view for deleting resources."""

    template_name = 'searchlist/delete_resource.html'
    success_message = "Resource was deleted successfully."
    model = Resource
    success_url = reverse_lazy('home')


class HomePageView(ListView):
    """Class home page view."""

    template_name = "searchlist/home.html"
    model = Resource

    def get_context_data(self, **kwargs):
        """Get context to populate page with resources."""
        context = super(HomePageView, self).get_context_data(**kwargs)
        # import pdb; pdb.set_trace()
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


class ResourceDetailView(DetailView):
    """Detail view for one organization."""

    template_name = "searchlist/resource_detail.html"
    model = Resource
    context_object_name = "resource"
    # {% for tag in resource.tags.all %}
    # <a href="{% url "search:tagged" tag.slug %}">{{ tag }}</a>,
    # {% endfor %}


# class resource_list(FilterView):
#     """Filter view for our resource list."""

#     f = ResourceFilter(reques.GET, queryset=Resource.objects.all())
#     return render(request, 'searchlist/template.html', {'filter: f'})

