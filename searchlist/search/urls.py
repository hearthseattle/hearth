"""URLs for the search app."""

from django.conf.urls import url

from search.views import TagListView, OrgListView, OrgDetailView

urlpatterns = [
    url(r'^$', OrgListView.as_view(), name="org_list"),
    url(r'^tagged/(?P<slug>[-\w]+)/$', TagListView.as_view(), name="tagged_orgs"),
    url(r'^(?P<id>\d+)$', OrgDetailView.as_view(), name="org_detail")
]
