from netbox.api.serializers import NetBoxModelSerializer
from .. import models

class GenericObjectTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericObjectType
        fields = '__all__'

class GenericObjectSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericObject
        fields = '__all__'

class RelationshipTypeSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.RelationshipType
        fields = '__all__'

class GenericRelationshipSerializer(NetBoxModelSerializer):
    class Meta:
        model = models.GenericRelationship
        fields = '__all__'
