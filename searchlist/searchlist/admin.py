"""Customize and register admin view."""
from django.contrib import admin
from searchlist.models import Resource


class ResourcesAdmin(admin.ModelAdmin):
    """Just show organization name in resources model admin."""

    list_display = ["org_name"]

admin.site.register(Resource, ResourcesAdmin)
