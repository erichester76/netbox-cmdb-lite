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
        help_text="Select an object type to load its dynamic attributes."
    )

    class Meta:
        model = models.GenericObject
        fields = ["name", "object_type", "metadata"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        object_type = instance.object_type if instance else self.initial.get("object_type")

        # Dynamically add fields for the attributes based on the object type
        if object_type and object_type.attributes:
            for attribute in object_type.attributes:
                field_name = f"metadata_{attribute['name']}"
                field_label = attribute["name"].capitalize()
                field_type = attribute["type"]

                if field_type == "string":
                    self.fields[field_name] = forms.CharField(
                        label=field_label,
                        required=False,
                        initial=instance.metadata.get(attribute["name"], "") if instance else ""
                    )
                elif field_type == "integer":
                    self.fields[field_name] = forms.IntegerField(
                        label=field_label,
                        required=False,
                        initial=instance.metadata.get(attribute["name"], 0) if instance else 0
                    )
                elif field_type == "boolean":
                    self.fields[field_name] = forms.BooleanField(
                        label=field_label,
                        required=False,
                        initial=instance.metadata.get(attribute["name"], False) if instance else False
                    )
                elif field_type == "multi-choice":
                    # Multi-choice can be extended to dynamically load choices
                    self.fields[field_name] = forms.ChoiceField(
                        label=field_label,
                        required=False,
                        choices=[("option1", "Option 1"), ("option2", "Option 2")],
                        initial=instance.metadata.get(attribute["name"], "option1") if instance else "option1"
                    )

    def clean(self):
        """
        Validate dynamic fields and save them into the metadata field.
        """
        cleaned_data = super().clean()
        metadata = {}
        if self.instance.object_type and self.instance.object_type.attributes:
            for attribute in self.instance.object_type.attributes:
                field_name = f"metadata_{attribute['name']}"
                if field_name in cleaned_data:
                    metadata[attribute["name"]] = cleaned_data[field_name]

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
