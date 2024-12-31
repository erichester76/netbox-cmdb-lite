from netbox.models import NetBoxModel
from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Category(NetBoxModel):
    name = models.CharField(max_length=100, unique=True, help_text="Name of the category")
    description = models.TextField(blank=True, help_text="Optional description for the category")

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("plugins:netbox_cmdb_lite:category", kwargs={'pk': self.pk})
    
class GenericObjectType(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    attributes = models.JSONField(
        default=list,
        blank=True,
        null=True,
        help_text="Define the fields and their types for this object type."
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="object_types",
        help_text="Category this object type belongs to"
    )
    relationships = models.JSONField(
        default=list, 
        blank=True, 
        null=True,
        help_text="Define the relationships and their types for this object type."
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("plugins:netbox_cmdb_lite:genericobjecttype", kwargs={'pk': self.pk})

class GenericObject(NetBoxModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    object_type = models.ForeignKey(GenericObjectType, on_delete=models.CASCADE)
    metadata = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Values for the dynamic attributes defined by the object type."
    )
    def __str__(self):
        return f"{self.name} ({self.object_type.name})"
    
    def get_absolute_url(self):
        return reverse("plugins:netbox_cmdb_lite:genericobject", kwargs={'pk': self.pk})

class RelationshipType(NetBoxModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional description of the relationship type

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("plugins:netbox_cmdb_lite:relationshiptype", kwargs={'pk': self.pk})
    
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

    def get_absolute_url(self):
        return reverse("plugins:netbox_cmdb_lite:genericrelationship", kwargs={'pk': self.pk})