"""Organization Profile View."""


from django.contrib.auth.models import User
from search.models import SearchProfile
from django.views.generic import DetailView, ListView
from django.shortcuts import render


# class OrgProfileView(request):
#     """Organization profile."""

#     template_name = "search/org_profile.html"
#     model = SearchProfile

#     def get(self, request, *args, **kwargs):
#         """."""
#         user = request.user
#         return self.render_to_response({"user": user})
def org_detail(request):
    """Detail view for one organization."""
    return render(request, "search/org_profile.html")   


class TagListView(ListView):
    """Display a list of tagged organizations."""

    template_name = "search/org_list.html"
    model = SearchProfile
    context_object_name = "orgs"

    def get_queryset(self):
        """Get all organizations in category."""
        return SearchProfile.active.filter(tags_slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context["tag"] = self.kwargs.get("slug")
        return context
