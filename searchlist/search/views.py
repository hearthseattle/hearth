"""Organization Profile View."""


from django.contrib.auth.models import User
from search.models import SearchProfile
from django.views.generic import DetailView, ListView
from django.shortcuts import render


class OrgListView(ListView):
    """Organization profile."""

    template_name = "search/org_list.html"
    model = SearchProfile
    context_object_name = "orgs"


def org_detail(request, id):
    """Detail view for one organization."""
    return render(request, "search/org_detail.html")


class TagListView(ListView):
    """Display a list of tagged organizations."""

    template_name = "search/org_list.html"

    def get_queryset(self):
        """Get all organizations in category."""
        return SearchProfile.active.filter(tags_slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        """."""
        context = super(TagListView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        return context
