"""View page for our homeless to hearth app."""
from __future__ import unicode_literals
from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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
from searchlist.models import (
    Resource,
    ResourceTag,
    SERVICES
)
from taggit.models import Tag


class CreateResource(LoginRequiredMixin, CreateView):
    """Class-based view to create new resources."""

    template_name = 'searchlist/resource_form.html'
    form_class = ResourceForm
    success_url = reverse_lazy('home')
    tag_fields = ResourceTag.objects.values_list('family', flat=True).distinct()
    exclude = ['created_by']

    def form_valid(self, form):
        """Add the tags through fields instead of a text area."""
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        for field in self.request.POST:
            if field in self.tag_fields:
                tag = ResourceTag.objects.get(family=field, value=self.request.POST[field])
                self.object.tags.add(tag)
        return HttpResponseRedirect(self.get_success_url())


class EditResource(LoginRequiredMixin, UpdateView):
    """Class-based view to edit resources."""

    model = Resource
    template_name = 'searchlist/resource_form.html'
    form_class = ResourceForm
    success_url = reverse_lazy('home')
    tag_fields = ResourceTag.objects.values_list('family', flat=True).distinct()

    def get_object(self, *args, **kwargs):
        """Implement permission check."""
        obj = super().get_object(*args, **kwargs)
        if not obj.created_by == self.request.user or self.request.user.is_staff:
            raise PermissionDenied
        return obj

    def get_form_kwargs(self):
        """
        Override get_form_kwargs, get all the tags on the edited resource,
        get the form_class choices, find the tag in the resources tags and
        get the index of that tag, and set the initial value of the field
        to it's choice label.
        """
        resource_id = self.kwargs['pk']
        resource_tags = Resource.objects.get(id=resource_id).tags.all().values_list('family', 'value')
        edit_form = self.form_class()
        edit_form_fields = edit_form.fields
        for field in self.tag_fields:
            choices = edit_form_fields[field].choices
            tags, selections = zip(*choices)
            intersection = [(t[0], t[1]) for t in tags if t in resource_tags]
            print('choices is {}'.format(choices))
            print('tags, selections: {}, {}'.format(tags, selections))
            print('intersection is {}'.format(intersection))
            if isinstance(edit_form_fields[field],
                          forms.fields.MultipleChoiceField):
                self.initial[field] = intersection
            else:
                self.initial[field] = intersection[0]

        return super(EditResource, self).get_form_kwargs()

    def form_valid(self, form):
        """Save form if valid."""
        self.object = form.save()
        Resource.objects.get(id=self.kwargs['pk']).tags.clear()
        for field in self.request.POST:
            if field in self.tag_fields:
                tag = ResourceTag.objects.get(family=field, value=self.request.POST[field])
                self.object.tags.add(tag)
        return HttpResponseRedirect(self.get_success_url())

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
