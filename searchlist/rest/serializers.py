"""Serialize our resource models."""
from searchlist.models import Resource
from rest_framework import serializers
from taggit_serializer.serializers import (TaggitSerializer,
                                           TagListSerializerField)


class ResourceSerializer(TaggitSerializer,
                         serializers.HyperlinkedModelSerializer):
    """Serialize our models into JSON."""

    tags = TagListSerializerField()

    class Meta:
        """Reference the model, and we want all fields."""

        model = Resource
        fields = '__all__'
