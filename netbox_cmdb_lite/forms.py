from netbox.forms import NetBoxModelForm
from django.contrib.contenttypes.models import ContentType
from django import forms
from . import models
from utilities.forms.fields import DynamicModelChoiceField, JSONField

class GenericObjectTypeForm(NetBoxModelForm):
    attributes = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 5,
            "placeholder": "Attributes will be populated dynamically using the UI below."
        }),
        required=False,
        label="Attributes (Dynamic)"
    )

    class Meta:
        model = models.GenericObjectType
        fields = ["name", "attributes"]

    def clean_attributes(self):
        """
        Validate and clean the attributes field to ensure it contains valid JSON.
        """
        import json
        attributes = self.cleaned_data.get("attributes", "[]")
        try:
            parsed_attributes = json.loads(attributes)
            # Validate each attribute
            for attr in parsed_attributes:
                if not isinstance(attr, dict) or "name" not in attr or "type" not in attr:
                    raise forms.ValidationError("Each attribute must include 'name' and 'type'.")
                if attr["type"] not in ["string", "integer", "boolean", "multi-choice"]:
                    raise forms.ValidationError(f"Invalid type '{attr['type']}' for attribute '{attr['name']}'.")
            return parsed_attributes
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"Invalid JSON: {e}")

        
class GenericObjectForm(NetBoxModelForm):
    object_type = forms.ModelChoiceField(
        queryset=models.GenericObjectType.objects.all(),
        label="Object Type",
        required=True,
        help_text="Select an object type to load its attributes dynamically."
    )
    metadata = forms.JSONField(
        label="Attributes",
        required=False,
        help_text="Enter values for the attributes defined in the selected object type."
    )

    class Meta:
        model = models.GenericObject
        fields = ["name", "object_type", "metadata"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance and instance.object_type:
            keys = instance.object_type.attributes
            for key in keys:
                self.fields[f"metadata_{key}"] = forms.CharField(
                    label=key.capitalize(),
                    required=False,
                    initial=instance.metadata.get(key, "") if instance.metadata else ""
                )

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
