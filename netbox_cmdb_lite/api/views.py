from netbox.api.viewsets import NetBoxModelViewSet
from ..models import ObjectType, GenericObject, RelationshipType, GenericRelationship
from .serializers import (
    ObjectTypeSerializer,
    GenericObjectSerializer,
    RelationshipTypeSerializer,
    GenericRelationshipSerializer,
)

class ObjectTypeViewSet(NetBoxModelViewSet):
    queryset = ObjectType.objects.all()
    serializer_class = ObjectTypeSerializer

class GenericObjectViewSet(NetBoxModelViewSet):
    queryset = GenericObject.objects.all()
    serializer_class = GenericObjectSerializer

class RelationshipTypeViewSet(NetBoxModelViewSet):
    queryset = RelationshipType.objects.all()
    serializer_class = RelationshipTypeSerializer

class GenericRelationshipViewSet(NetBoxModelViewSet):
    queryset = GenericRelationship.objects.all()
    serializer_class = GenericRelationshipSerializer
