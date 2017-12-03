"""Serialize our resource models."""
from searchlist.models import Resource
from rest_framework import serializers


class ResourceSerializer(serializers.ModelSerializer):
    """Serialize our models into JSON."""

    class Meta:
        model = Resource
        fields = '__all__'
