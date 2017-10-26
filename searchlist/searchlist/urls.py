"""searchlist URL Configuration."""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from rest.views import ResourceViewSet
from searchlist.views import (
    HomePageView,
    CreateResource,
    EditResource,
    ResourceDetailView,
    DeleteResource
)

router = routers.DefaultRouter()
router.register(r'resources', ResourceViewSet)

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^adminhearth/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.admin_approval.urls')),
    url(r'^resource/new/$', CreateResource.as_view(), name='create_resource'),
    url(r'^resource/(?P<pk>\d+)/edit/$', EditResource.as_view(), name='edit_resource'),
    url(r'^resource/(?P<pk>\d+)$', ResourceDetailView.as_view(), name="resource_detail"),
    url(r'^resource/(?P<pk>\d+)/delete/$',
        DeleteResource.as_view(success_message="The resource has been successfully deleted"),
        name="delete"),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
