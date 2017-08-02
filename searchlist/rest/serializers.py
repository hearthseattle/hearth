"""Serialize our resource models."""
from searchlist.models import Resource
from rest_framework import serializers


class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
