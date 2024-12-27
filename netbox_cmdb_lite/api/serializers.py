from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from .. import models 
from django.contrib.contenttypes.models import ContentType

# Serializer for GenericObjectType
class GenericObjectTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericObjectType
        fields = ['id', 'name', 'attributes', 'created', 'last_updated']

# Serializer for GenericObject
class GenericObjectSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericObject
        fields = ['id', 'name', 'object_type', 'metadata', 'created', 'last_updated']

# Serializer for RelationshipType
class RelationshipTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.RelationshipType
        fields = ['id', 'name', 'description', 'created', 'last_updated']

# Serializer for GenericRelationship
class GenericRelationshipSerializer(NetBoxModelSerializer):
    source_content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    source_object_id = serializers.IntegerField()
    target_content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    target_object_id = serializers.IntegerField()

    class Meta:
        model = models.GenericRelationship
        fields = [
            'id', 'source_content_type', 'source_object_id',
            'target_content_type', 'target_object_id',
            'relationship_type', 'attributes', 'created', 'last_updated'
        ]
