from netbox.forms import NetBoxModelForm
from django.contrib.contenttypes.models import ContentType
from django import forms
import jsonschema
from jsonschema.exceptions import ValidationError
from . import models

class GenericObjectTypeForm(NetBoxModelForm):
    class Meta:
        model = models.GenericObjectType
        fields = ["name", "attributes"]

class GenericObjectForm(NetBoxModelForm):
    class Meta:
        model = models.GenericObject
        fields = ["name", "object_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance and instance.object_type and instance.object_type.attributes:
            attributes = instance.object_type.attributes
            for attr_name, attr_meta in attributes.get("properties", {}).items():
                field_type = attr_meta.get("type")
                required = attr_name in attributes.get("required", [])
                if field_type == "string":
                    self.fields[attr_name] = forms.CharField(
                        label=attr_name.capitalize(),
                        required=required,
                        initial=instance.metadata.get(attr_name, "") if instance.metadata else "",
                    )
                elif field_type == "integer":
                    self.fields[attr_name] = forms.IntegerField(
                        label=attr_name.capitalize(),
                        required=required,
                        initial=instance.metadata.get(attr_name, 0) if instance.metadata else 0,
                    )

    def clean(self):
        cleaned_data = super().clean()
        metadata = {}
        for field_name, value in cleaned_data.items():
            if field_name not in ["name", "object_type"]:
                metadata[field_name] = value
        self.cleaned_data["metadata"] = metadata
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
