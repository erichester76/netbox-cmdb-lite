from netbox.api.serializers import NetBoxModelSerializer
from .. import models

class ObjectTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericObjectType
        fields = ['id', 'name', 'attributes']

class GenericObjectSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericObject
        fields = ['id', 'name', 'object_type', 'metadata']

class RelationshipTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.RelationshipType
        fields = ['id', 'name', 'description']

class GenericRelationshipSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericRelationship
        fields = ['id', 'source_content_type', 'source_object_id', 'target_content_type', 'target_object_id', 'relationship_type', 'attributes']
