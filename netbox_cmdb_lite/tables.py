from netbox.tables import NetBoxTable
import django_tables2 as tables
from . import models

class GenericObjectTypeTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.GenericObjectType
        fields = ("pk", "name")

class GenericObjectTable(NetBoxTable):
    name = tables.Column(linkify=True)
    object_type = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.GenericObject
        fields = ("pk", "name", "object_type")

class RelationshipTypeTable(NetBoxTable):
    name = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.RelationshipType
        fields = ("pk", "name")

class GenericRelationshipTable(NetBoxTable):
    source = tables.Column(linkify=True)
    target = tables.Column(linkify=True)
    relationship_type = tables.Column(linkify=True)

    class Meta(NetBoxTable.Meta):
        model = models.GenericRelationship
        fields = ("pk", "source", "target", "relationship_type")