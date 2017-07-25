"""Views for creating and updating resources."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from search.models import Resource


class CreateResource(LoginRequiredMixin, CreateView):
    """Class-based view to create new resources."""

    template_name = 'resource_admins/resource_form.html'
    model = Resource
    fields = ['main_category', 'ratings', 'age_range', 'org_name',
              'description', 'location', 'website',
              'phone_number', 'tags']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Save form if valid."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(CreateResource, self).form_valid(form)


class EditResource(LoginRequiredMixin, UpdateView):
    """Class-based view to edit resources."""

    template_name = 'resource_admins/resource_form.html'
    model = Resource
    fields = ['main_category', 'ratings', 'age_range', 'org_name',
              'description', 'location', 'website',
              'phone_number', 'tags']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Save form if valid."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(EditResource, self).form_valid(form)


class DeleteResource(LoginRequiredMixin, DeleteView):
    """Class-based view for deleting resources."""

    template_name = 'resource_admins/delete_resource.html'
    model = Resource
    success_url = reverse_lazy('home')
