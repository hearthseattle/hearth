"""Customize and register admin view."""
from django.contrib import admin
from searchlist.models import (
    Resource,
    Language,
    Service
)


class ResourcesAdmin(admin.ModelAdmin):
    """Just show organization name in resources model admin."""

    list_display = ["name"]


admin.site.register(Language)
admin.site.register(Service)
admin.site.register(Resource, ResourcesAdmin)
