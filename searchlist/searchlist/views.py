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
# from searchlist.forms import ResourceForm
# from django.shortcuts import render_to_response


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
        MAIN_CATEGORY = [
            ("Crisis", "Crisis"),
            ("Addiction", "Addiction"),
            ("Childcare", "Childcare"),
            ("Youth Services", "Youth Services"),
            ("Veteran", "Veteran"),
            ("Rehabilitation", "Rehabilitation"),
            ("Mental/Physical Disability", "Mental/Physical Disability"),
            ("Education", "Education"),
            ("Employment", "Employment"),
            ("Finances", "Finances"),
            ("Clothing/Housewares", "Clothing/Housewares"),
            ("Food", "Food"),
            ("Healthcare", "Healthcare"),
            ("Shelter", "Shelter"),
            ("Legal", "Legal"),
            ("Identification", "Identification"),
            ("Spiritual", "Spiritual")
        ]

        context = super(HomePageView, self).get_context_data(**kwargs)
        context['choices'] = [category[0] for category in MAIN_CATEGORY]
        # import pdb; pdb.set_trace()
        return context


# class SearchFormView(ListView):
#     """Display a Resource list filtered by a search query."""

#     def get_queryset(self):
#         """Get a query for our search."""
#         result = super(SearchFormView, self).get_queryset()

#         query = self.request.GET.get('q')
#         if query:
#             query_list = query.split()
#             result = result.filter(
#                 reduce(operator.and_,
#                        (Q(tags__icontains=q) for q in query_list)) |
#                 reduce(operator.and_,
#                        (Q(tags__icontains=q) for q in query_list))
#             )
#         return result


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


# def filter_resources(request=None, tags=None):
#     query = Resource.objects.filter()
#     if tags and tags != "All tags":
#         try:
#             tag = tags.objects.get(name=tags)
#             query = query.filter(tags=tag)
#         except:
#             return None
#     return query


# def resource_list(request):
#     d = getVariables(request)
#     if request.method == "GET":
#         form = ResourceForm(request.GET)
#         try:
#             t_name = request.GET["tags"]
#         except:
#             t_name = None
#         d["t_name"] = t_name
#         try:
#             resources = filter_resources(request=request, tags=t_name)
#         except Exception:
#             return error404(request)
#         if resources is None:
#             return error404(request)
#         if len(resources) == 0:
#             d["not_found"] = "Oh hi there."
#     else:
#         form = ResourceForm()
#     return render_to_response('searchlist/Resource_filter.html', d, context_instance=RequestContext(request))
