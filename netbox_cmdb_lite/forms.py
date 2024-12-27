from netbox.forms import NetBoxModelForm
from django.contrib.contenttypes.models import ContentType
from django import forms
from . import models
from utilities.forms.fields import DynamicModelChoiceField, JSONField
import json

class GenericObjectTypeForm(NetBoxModelForm):
    class Meta:
        model = models.GenericObjectType
        fields = ["name", "attributes"]

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

        
from django import forms
from utilities.forms.fields import DynamicModelChoiceField, JSONField
from .models import GenericObject, GenericObjectType

class GenericObjectForm(forms.ModelForm):
    object_type = DynamicModelChoiceField(
        queryset=GenericObjectType.objects.all(),
        label="Object Type",
        required=True,
        help_text="Select an object type to load attributes dynamically."
    )
    metadata = JSONField(
        label="Attributes",
        required=False,
        help_text="Dynamic attributes based on the selected object type."
    )

    class Meta:
        model = GenericObject
        fields = ["name", "object_type", "metadata"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        object_type = instance.object_type if instance else self.data.get("object_type")

        if object_type:
            object_type_instance = (
                object_type if isinstance(object_type, GenericObjectType) else GenericObjectType.objects.get(pk=object_type)
            )
            self._add_dynamic_fields(object_type_instance)

    def _add_dynamic_fields(self, object_type):
        # Dynamically add fields based on the object type's attributes
        for attribute in object_type.attributes:
            field_name = attribute["name"]
            field_type = attribute["type"]

            if field_type == "string":
                self.fields[field_name] = forms.CharField(
                    label=field_name.capitalize(),
                    required=False,
                    initial=self.instance.metadata.get(field_name, "") if self.instance and self.instance.metadata else ""
                )
            elif field_type == "integer":
                self.fields[field_name] = forms.IntegerField(
                    label=field_name.capitalize(),
                    required=False,
                    initial=self.instance.metadata.get(field_name, 0) if self.instance and self.instance.metadata else 0
                )
            elif field_type == "boolean":
                self.fields[field_name] = forms.BooleanField(
                    label=field_name.capitalize(),
                    required=False,
                    initial=self.instance.metadata.get(field_name, False) if self.instance and self.instance.metadata else False
                )
            elif field_type == "multi-choice":
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=[(opt, opt) for opt in attribute.get("options", [])],
                    label=field_name.capitalize(),
                    required=False,
                    initial=self.instance.metadata.get(field_name, []) if self.instance and self.instance.metadata else []
                )
            elif field_type == "foreign-key":
                # Handle foreign key references dynamically
                self.fields[field_name] = forms.CharField(
                    label=f"{field_name.capitalize()} (Reference)",
                    required=False,
                    initial=self.instance.metadata.get(field_name, "") if self.instance and self.instance.metadata else ""
                )
                
    def clean(self):
        # Ensure metadata is constructed from dynamic fields
        cleaned_data = super().clean()
        metadata = {}
        for field_name in self.fields:
            if field_name not in ["name", "object_type", "metadata"]:
                metadata[field_name] = cleaned_data.get(field_name)
        cleaned_data["metadata"] = metadata
        return cleaned_data

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
