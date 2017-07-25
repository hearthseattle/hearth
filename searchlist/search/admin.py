"""Docstring for superuser."""


from django.contrib import admin
from search.models import Resource


class UserAdmin(admin.ModelAdmin):
    """Display organizations with descriptions."""

    list_display = ('org_name', 'main_category', 'ratings', 'age_range')
    list_filter = ('main_category',)

admin.site.register(Resource, UserAdmin)
