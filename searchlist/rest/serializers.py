"""Serialize our resource models."""
from searchlist.models import Resource
from rest_framework import serializers


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    """Serialize our models into JSON."""

    class Meta:
        """Reference the model, and we want all fields."""

        model = Resource
        fields = '__all__'
