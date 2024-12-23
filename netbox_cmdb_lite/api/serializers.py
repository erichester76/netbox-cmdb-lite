from netbox.api.serializers import NetBoxModelSerializer
from ..models import ObjectType, GenericObject, RelationshipType, GenericRelationship

class ObjectTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = ObjectType
        fields = ['id', 'name', 'attributes']

class GenericObjectSerializer(NetBoxModelSerializer):
    class Meta:
        model = GenericObject
        fields = ['id', 'name', 'object_type', 'metadata']

class RelationshipTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = RelationshipType
        fields = ['id', 'name', 'description']

class GenericRelationshipSerializer(NetBoxModelSerializer):
    class Meta:
        model = GenericRelationship
        fields = ['id', 'source_content_type', 'source_object_id', 'target_content_type', 'target_object_id', 'relationship_type', 'attributes']
