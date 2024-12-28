from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from .. import models 
from django.contrib.contenttypes.models import ContentType

# Serializer for GenericObjectType
class GenericObjectTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericObjectType
        fields = '__all__'

# Serializer for GenericObject
class GenericObjectSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericObject
        fields = '__all__'


# Serializer for RelationshipType
class RelationshipTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.RelationshipType
        fields = '__all__'


# Serializer for GenericRelationship
class GenericRelationshipSerializer(NetBoxModelSerializer):
    source_content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    source_object_id = serializers.IntegerField()
    target_content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    target_object_id = serializers.IntegerField()

    class Meta:
        model = models.GenericRelationship
        fields = '__all__'

