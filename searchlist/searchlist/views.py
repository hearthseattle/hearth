"""View page for our homeless to hearth app."""
from __future__ import unicode_literals
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
    FormMixin
)
from .forms import (
    ResourceForm,
    FilterForm
)
from searchlist.models import Resource


class CreateResource(LoginRequiredMixin, CreateView):
    """Class-based view to create new resources."""

    template_name = 'searchlist/resource_form.html'
    form_class = ResourceForm
    success_url = reverse_lazy('home')


class EditResource(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Class-based view to edit resources."""

    model = Resource
    template_name = 'searchlist/resource_form.html'
    form_class = ResourceForm
    success_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, **kwargs):
        """."""
        context = super(EditResource, self).get_context_data(**kwargs)
        context["edit"] = True
        return context

    def test_func(self):
        """Permission test using Django mixin."""
        user_created = self.get_object().created_by == self.request.user
        user_is_staff = self.request.user.is_staff
        return user_created or user_is_staff


class DeleteResource(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Class-based view for deleting resources."""

    template_name = 'searchlist/delete_resource.html'
    success_message = "Resource was deleted successfully."
    model = Resource
    success_url = reverse_lazy('home')
    raise_exception = True

    def test_func(self):
        """Permission test using Django mixin."""
        user_created = self.get_object().created_by == self.request.user
        user_is_staff = self.request.user.is_staff
        return user_created or user_is_staff


class HomePageView(FormMixin, ListView):
    """Class home page view."""

    template_name = "searchlist/home.html"
    model = Resource
    form_class = FilterForm

    def get_context_data(self, **kwargs):
        """Get context to populate page with resources."""
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['clear_nav_bar'] = True
        return context


class ResourceDetailView(DetailView):
    """Detail view for one organization."""

    template_name = "searchlist/resource_detail.html"
    model = Resource
    context_object_name = "resource"
