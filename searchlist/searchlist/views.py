"""View page for our homeless to hearth app."""
from __future__ import unicode_literals
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views import View
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
    SERVICES
)
from taggit.models import Tag


class CreateResource(LoginRequiredMixin, CreateView):
    """Class-based view to create new resources."""

    template_name = 'searchlist/resource_form.html'
    form_class = ResourceForm
    success_url = reverse_lazy('home')
    tag_fields = ['language', 'age', 'gender', 'citizenship',
                  'lgbtqia', 'sobriety', 'costs', 'case_managers',
                  'counselors', 'always_open', 'pets', 'various']

    def form_valid(self, form):
        """Add the tags through fields instead of a text area."""
        saved_model_form = form.save()
        for field in self.request.POST:
            if field in self.tag_fields:
                saved_model_form.tags.add(self.request.POST[field])
                saved_model_form.save()
        return super(CreateResource, self).form_valid(form)


class EditResource(LoginRequiredMixin, UpdateView):
    """Class-based view to edit resources."""

    model = Resource
    template_name = 'searchlist/resource_form.html'
    form_class = ResourceForm
    success_url = reverse_lazy('home')
    tag_fields = ['language', 'age', 'gender', 'citizenship',
                  'lgbtqia', 'sobriety', 'costs', 'case_managers',
                  'counselors', 'always_open', 'pets', 'various']

    def get_form_kwargs(self):
        """
        Override get_form_kwargs, get all the tags on the edited resource,
        get the form_class choices, find the tag in the resources tags and
        get the index of that tag, and set the initial value of the field
        to it's choice label.
        """
        resource_id = self.kwargs['pk']
        resource_tags = Resource.objects.get(id=resource_id).tags.names()
        edit_form = self.form_class()
        edit_form_fields = edit_form.fields
        for field in self.tag_fields:
            choices = edit_form_fields[field].choices
            tags, selections = zip(*choices)
            intersection = [tag for tag in tags if tag in resource_tags]
            if isinstance(edit_form_fields[field],
                          forms.fields.MultipleChoiceField):
                self.initial[field] = intersection
            else:
                self.initial[field] = intersection[0]

        return super(EditResource, self).get_form_kwargs()

    def form_valid(self, form):
        """Save form if valid."""
        resource_id = self.kwargs['pk']
        resource_tags = Resource.objects.get(id=resource_id).tags
        for field in form.changed_data:
            if field in self.tag_fields:
                if isinstance(form.fields[field],
                              forms.fields.MultipleChoiceField):
                    POST_list = self.request.POST.getlist(field)
                    for tag in POST_list:
                        if tag in resource_tags.names():
                            resource_tags.remove(form.initial[field])
                            form.save()
                    for tag in POST_list:
                        resource_tags.add(tag)
                        form.save()
                else:
                    choices = form.fields[field].choices
                    tags, selections = zip(*choices)
                    post = self.request.POST[field]
                    for tag in tags:
                        if tag in resource_tags.names():
                            resource_tags.remove(tag)
                            form.save()
                    resource_tags.add(post)
                    form.save()

                    # if post not in resource_tags.names():
                    #     resource_tags.

        # for field in form.changed_data:
        #     if field in self.tag_fields:
        #         if isinstance(form.initial[field], list):
        #                 for tag in form.initial[field]:
        #                     resource_tags.remove(tag)
        #                     form.save()
        #                 for tag in self.request.POST[field].getlist():
        #                     resource_tags.add(tag)
        #                     form.save()
        #         else:
        #             # if form.initial[field] != self.request.POST[field]:
        #             post_tags = self.request.POST.getlist('')
        #             for tag in resource_tags.names():
        #                 resource_tags.remove(form.initial[tag])
        #                 form.save()
        #             for tag in post_tags:
        #                     resource_tags.add(tag)
        #                     form.save()
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
