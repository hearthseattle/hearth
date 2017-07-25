"""Urls related to the creating and editing resources."""
from django.conf.urls import url
from .views import CreateResource, EditResource

urlpatterns = [
    url(r'^new/$', CreateResource.as_view(), name='create_resource'),
    url(r'^(?P<pk>\w+)/edit/$', EditResource.as_view(), name='edit_resource')
]
