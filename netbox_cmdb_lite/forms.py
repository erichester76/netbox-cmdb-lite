from django.contrib.contenttypes.models import ContentType
from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField, JSONField
from . import models



class CategoryForm(NetBoxModelForm):
    class Meta:
        model = models.Category
        fields = ["name", "description"]

class GenericObjectTypeForm(NetBoxModelForm):
    category = DynamicModelChoiceField(
        queryset=models.Category.objects.all(),
        label="Category",
        required=False,
        help_text="Select a category for this object type"
    )
    relationships = JSONField(
        label="Default Relationships",
        required=False,
        help_text="Define default relationships for this object type. Specify relationship types and allowed object types."
    )
    
    class Meta:
        model = models.GenericObjectType
        fields = ["name", "category", "attributes", "relationships"]

    def clean_attributes(self):
        attributes = self.cleaned_data.get("attributes", [])
        if not isinstance(attributes, list):
            raise forms.ValidationError("Attributes must be a list of dictionaries.")
        for attr in attributes:
            if not isinstance(attr, dict):
                raise forms.ValidationError("Each attribute must be a dictionary.")
            if "name" not in attr or "type" not in attr:
                raise forms.ValidationError("Each attribute must have a 'name' and 'type'.")
            if attr["type"] == "multi-choice" and "options" in attr:
                if not isinstance(attr["options"], list):
                    raise forms.ValidationError(f"Options for '{attr['name']}' must be a list.")
            if attr["type"] == "foreign-key" and "reference" in attr:
                if not isinstance(attr["reference"], str):
                    raise forms.ValidationError(f"Reference for '{attr['name']}' must be a string.")
        return attributes

    def clean_relationships(self):
        relationships = self.cleaned_data.get("relationships", [])
        if not isinstance(relationships, list):
            raise forms.ValidationError("Relationships must be a list of objects.")
        for relationship in relationships:
            if "relationship_type" not in relationship or "allowed_types" not in relationship:
                raise forms.ValidationError("Each relationship must include a 'relationship_type' and 'allowed_types'.")
            if not isinstance(relationship["relationship_type"], str):
                raise forms.ValidationError(f"Relationship 'type' must be a string. Found: {relationship['relationship_type']}")
            if not isinstance(relationship["allowed_types"], list):
                raise forms.ValidationError(f"'allowed_types' must be a list of strings. Found: {relationship['allowed_types']}")
            if not all(isinstance(typ, str) for typ in relationship["allowed_types"]):
                raise forms.ValidationError("All 'allowed_types' entries must be strings.")
        return relationships

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance", None)
        super().__init__(*args, **kwargs)

        # Prepare RelationshipType choices
        relationship_type_choices = [(rel.pk, rel.name) for rel in models.RelationshipType.objects.all()]

        # Prepare Allowed Object Type choices
        allowed_type_choices = []
        for obj in models.GenericObjectType.objects.all():
            allowed_type_choices.append((f"cmdb:{obj.pk}", f"CMDB: {obj.name}"))
        netbox_cts = ContentType.objects.filter(app_label__in=['dcim', 'virtualization', 'ipam', 'tenancy'])
        for ct in netbox_cts:
            allowed_type_choices.append((f"netbox:{ct.pk}", f"NetBox: {ct.app_label}.{ct.model}"))

        # Dynamically populate field choices
        self.relationship_type_choices = relationship_type_choices
        self.allowed_type_choices = allowed_type_choices

        # Set initial data for relationships when editing an instance
        self.initial_relationships = []
        if instance and instance.relationships:
            for relationship in instance.relationships:
                self.initial_relationships.append({
                    "relationship_type": relationship.get("relationship_type"),
                    "allowed_types": relationship.get("allowed_types", [])
                })

                
    def save(self, commit=True):
        instance = super().save(commit=False)

        # Collect all relationships
        relationships = []
        for i in range(len(self.initial_relationships) + 1):  # Adjust range for dynamically added rows
            relationship_type = self.data.get(f"relationship_type_{i}")
            allowed_types = self.data.getlist(f"allowed_types_{i}")
            if relationship_type:  # Only add if relationship_type exists
                relationships.append({
                    "relationship_type": relationship_type,
                    "allowed_types": allowed_types,
                })

        # Save relationships JSON
        instance.relationships = relationships

        if commit:
            instance.save()

        return instance
                    
                
class GenericObjectForm(forms.ModelForm):
    object_type = DynamicModelChoiceField(
        queryset=models.GenericObjectType.objects.all(),
        label="Object Type",
        required=True,
        help_text="Select the object type to load fields dynamically."
    )
    metadata = JSONField(
        label="Attributes",
        required=False,
        help_text="Dynamic attributes based on the selected object type."
    )

    class Meta:
        model = models.GenericObject
        fields = ["name", "object_type", "metadata"]

    def clean_metadata(self):
        # Ensure metadata is a valid JSON object
        metadata = self.cleaned_data.get("metadata", {})
        if not isinstance(metadata, dict):
            raise forms.ValidationError("Metadata must be a valid JSON object.")
        return metadata


class RelationshipTypeForm(NetBoxModelForm):
    class Meta:
        model = models.RelationshipType
        fields = ["name", "description"]
        
class RelationshipForm(NetBoxModelForm):
    class Meta:
        model = models.GenericRelationship
        fields = ['source_content_type', 'source_object_id', 'target_content_type', 'target_object_id', 'relationship_type', 'attributes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        allowed_models = ['device', 'rack', 'genericobject']
        self.fields['source_content_type'].queryset = ContentType.objects.filter(model__in=allowed_models)
        self.fields['target_content_type'].queryset = ContentType.objects.filter(model__in=allowed_models)
