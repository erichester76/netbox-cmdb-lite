from django.contrib.contenttypes.models import ContentType
from django import forms
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField
from . import models

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
        to_field_name="name",  # Explicitly use the `name` field
        help_text="Select the object type to load fields dynamically.",
    )

    class Meta:
        model = models.GenericObject
        fields = ["name", "object_type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        object_type = cleaned_data.get("object_type")
        if not object_type:
            raise forms.ValidationError("An object type must be selected.")
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
