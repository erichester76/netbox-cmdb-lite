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
    
    class Meta:
        model = models.GenericObjectType
        fields = ["name", "category", "attributes"]

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
