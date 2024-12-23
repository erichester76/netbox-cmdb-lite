from netbox.api.viewsets import NetBoxModelViewSet
from .. import models
from . import serializers

class GenericObjectTypeViewSet(NetBoxModelViewSet):
    queryset = models.GenericObjectType.objects.all()
    serializer_class = serializers.ObjectTypeSerializer

class GenericObjectViewSet(NetBoxModelViewSet):
    queryset = models.GenericObject.objects.all()
    serializer_class = serializers.GenericObjectSerializer

class RelationshipTypeViewSet(NetBoxModelViewSet):
    queryset = models.RelationshipType.objects.all()
    serializer_class = serializers.RelationshipTypeSerializer

class GenericRelationshipViewSet(NetBoxModelViewSet):
    queryset = models.GenericRelationship.objects.all()
    serializer_class = serializers.GenericRelationshipSerializer
