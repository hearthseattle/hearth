"""Views for serializers."""
from rest_framework import viewsets
from rest.serializers import ResourceSerializer

from searchlist.models import Resource
from rest.permissions import ResourcePermission


class ResourceViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to view or edit resources."""

    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = (ResourcePermission,)
