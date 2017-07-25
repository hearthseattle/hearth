"""Organization Profile View."""


from search.models import Resource
from django.views.generic import DetailView, ListView


class OrgListView(ListView):
    """Organization profile."""

    template_name = "search/org_list.html"
    model = Resource
    context_object_name = "orgs"


class OrgDetailView(DetailView):
    """Detail view for one organization."""

    template_name = "search/org_detail.html"
    model = Resource
    context_object_name = "org"


# class TagListView(ListView):
#     """Display a list of tagged organizations."""

    template_name = "serach/org_list.html"

#     def get_queryset(self):
#         """Get all organizations in category."""
#         return Resource.objects.filter(tags_slug=self.kwargs.get("slug")).all()

#     def get_context_data(self, **kwargs):
#         """."""
#         context = super(TagListView, self).get_context_data(**kwargs)
#         context["tag"] = self.kwargs.get("slug")
#         return context
