from netbox.models import NetBoxModel
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class ObjectType(NetBoxModel):
    name = models.CharField(max_length=50, unique=True)
    attributes = models.JSONField(blank=True, null=True)  # Define allowed attributes as JSON schema

    def __str__(self):
        return self.name

class GenericObject(NetBoxModel):
    name = models.CharField(max_length=100)
    object_type = models.ForeignKey(ObjectType, on_delete=models.CASCADE)
    metadata = models.JSONField(blank=True, null=True)  # Store dynamic attributes

    def __str__(self):
        return f"{self.name} ({self.object_type.name})"

class RelationshipType(NetBoxModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional description of the relationship type

    def __str__(self):
        return self.name
    
class GenericRelationship(NetBoxModel):
    source_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="source_relationships")
    source_object_id = models.PositiveIntegerField()
    source = GenericForeignKey('source_content_type', 'source_object_id')

    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="target_relationships")
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')

    relationship_type = models.ForeignKey(RelationshipType, on_delete=models.CASCADE)
    attributes = models.JSONField(blank=True, null=True)  # Store relationship-specific attributes

    def __str__(self):
        source_type = getattr(self.source_content_type.model_class(), '__name__', 'Unknown')
        target_type = getattr(self.target_content_type.model_class(), '__name__', 'Unknown')
        return f"{self.source} ({source_type}) -> {self.target} ({target_type}) ({self.relationship_type})"
