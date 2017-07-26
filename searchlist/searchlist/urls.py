"""searchlist URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from searchlist.views import (
    HomePageView,
    SearchFormView,
    CreateResource,
    EditResource,
    ResourceDetailView,
    DeleteResource
)
from django.conf import settings
from django.conf.urls.static import static
from django_filters.views import FilterView
from searchlist.models import Resource


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(
        template_name='registration/login.html'),
        name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(),
        name='logout'),
    url(r'^$', SearchFormView.as_view(), name='search_results'),
    url(
        r'^resource/new/$',
        CreateResource.as_view(),
        name='create_resource'
    ),
    url(
        r'^resource/(?P<pk>\d+)/edit/$',
        EditResource.as_view(),
        name='edit_resource'
    ),
    url(
        r'^resource/(?P<pk>\d+)$',
        ResourceDetailView.as_view(),
        name="resource_detail"
    ),
    url(
        r'^resource/(?P<pk>\d+)/delete/$',
        DeleteResource.as_view(
            success_message="The resource has been successfully deleted"
        ),
        name="delete"
    ),
    url(
        r'^resource_list/$', 
        FilterView.as_view(model=Resource)
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
