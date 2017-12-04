"""View page for our homeless to hearth app."""
from __future__ import unicode_literals
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from .forms import (
    ResourceForm,
    FilterForm
)
from searchlist.models import Resource
from searchlist.models import SERVICES
from taggit.models import Tag


class CreateResource(LoginRequiredMixin, CreateView):
    """Class-based view to create new resources."""

    template_name = 'searchlist/resource_form.html'
    form_class = ResourceForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Add the tags through fields instead of a text area."""
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class EditResource(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Class-based view to edit resources."""

    model = Resource
    template_name = 'searchlist/resource_form.html'
    form_class = ResourceForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Save form if valid."""
        return super(EditResource, self).form_valid(form)

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


class DeleteResource(LoginRequiredMixin, DeleteView):
    """Class-based view for deleting resources."""

    template_name = 'searchlist/delete_resource.html'
    success_message = "Resource was deleted successfully."
    model = Resource
    success_url = reverse_lazy('home')

    def get_object(self, *args, **kwargs):
        """Implement permission check."""
        obj = super().get_object(*args, **kwargs)
        if not obj.created_by == self.request.user or self.request.user.is_staff:
            raise PermissionDenied
        return obj

    def delete(self, request, *args, **kwargs):
        """Delete override to add a success message."""
        messages.success(self.request, self.success_message)
        return super(DeleteResource, self).delete(request, *args, **kwargs)


class HomePageView(ListView):
    """Class home page view."""

    template_name = "searchlist/home.html"
    model = Resource
    form_class = FilterForm

    def get_context_data(self, **kwargs):
        """Get context to populate page with resources."""
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['choices'] = [service[1] for service in SERVICES]
        context['form'] = self.form_class()
        context['clear_nav_bar'] = True
        context['tags'] = Tag.objects.all()
        return context


class ResourceDetailView(DetailView):
    """Detail view for one organization."""

    template_name = "searchlist/resource_detail.html"
    model = Resource
    context_object_name = "resource"
