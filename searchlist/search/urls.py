"""URLs for the search app."""

from django.conf.urls import url

from search.views import TagListView, OrgListView, org_detail

urlpatterns = [
    url(r'^$', OrgListView.as_view(), name="org_list"),
    url(r'^tagged/(?P<slug>[-\w]+)/$', TagListView.as_view(), name="tagged_orgs"),
    url(r'^(?P<id>\d+)$', org_detail, name="org_detail")
]
