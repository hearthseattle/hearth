from django.contrib import admin
from searchlist.models import Resource


class ResourcesAdmin(admin.ModelAdmin):

    list_display = ("org_name")

admin.site.register(Resource)
