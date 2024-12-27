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

class GenericObjectForm(forms.ModelForm):
    object_type = DynamicModelChoiceField(
        queryset=models.GenericObjectType.objects.all(),
        label="Object Type",
        required=True,
        help_text="Select the object type to load fields dynamically."
    )

    class Meta:
        model = models.GenericObject
        fields = ["name", "object_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = kwargs.get("instance", None)

        # Determine object_type from instance or initial data
        object_type = self.instance.object_type if self.instance else self.data.get("object_type")

        # If an object_type is set, dynamically add fields based on attributes
        if object_type:
            if isinstance(object_type, models.GenericObjectType):
                object_type_instance = object_type
            else:
                object_type_instance = models.GenericObjectType.objects.get(pk=object_type)
            self._add_dynamic_fields(object_type_instance)

    def _add_dynamic_fields(self, object_type):
        for attribute in object_type.attributes:
            field_name = attribute["name"]
            field_type = attribute["type"]

            # Add fields dynamically based on type
            if field_type == "string":
                self.fields[field_name] = forms.CharField(
                    label=field_name.capitalize(),
                    required=False,
                    initial=self.instance.metadata.get(field_name, "") if self.instance else ""
                )
            elif field_type == "integer":
                self.fields[field_name] = forms.IntegerField(
                    label=field_name.capitalize(),
                    required=False,
                    initial=self.instance.metadata.get(field_name, 0) if self.instance else 0
                )
            elif field_type == "boolean":
                self.fields[field_name] = forms.BooleanField(
                    label=field_name.capitalize(),
                    required=False,
                    initial=self.instance.metadata.get(field_name, False) if self.instance else False
                )
            elif field_type == "multi-choice":
                self.fields[field_name] = forms.MultipleChoiceField(
                    choices=[(opt, opt) for opt in attribute.get("options", [])],
                    label=field_name.capitalize(),
                    required=False,
                    initial=self.instance.metadata.get(field_name, []) if self.instance else []
                )
            elif field_type == "foreign-key":
                self.fields[field_name] = forms.CharField(
                    label=f"{field_name.capitalize()} (Reference)",
                    required=False,
                    initial=self.instance.metadata.get(field_name, "") if self.instance else ""
                )

    def clean(self):
        cleaned_data = super().clean()

        # Build metadata dynamically from dynamic fields
        metadata = {}
        for field_name in self.fields:
            if field_name not in ["name", "object_type"]:
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
