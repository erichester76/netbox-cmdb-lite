from netbox.forms import NetBoxModelForm
from django.contrib.contenttypes.models import ContentType
from django import forms
from . import models
from utilities.forms.fields import DynamicModelChoiceField, JSONField

class GenericObjectTypeForm(NetBoxModelForm):
    attributes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Enter attributes in JSON format or use the dynamic fields below.'
        }),
        label="Attributes (JSON)"
    )

    class Meta:
        model = models.GenericObjectType
        fields = ["name", "attributes"]

    def clean_attributes(self):
        """
        Validate and clean the attributes field to ensure it contains valid JSON.
        """
        import json
        attributes = self.cleaned_data.get("attributes", "{}")
        try:
            return json.loads(attributes)
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f"Invalid JSON: {e}")
        
class GenericObjectForm(NetBoxModelForm):
    object_type = DynamicModelChoiceField(
        queryset=models.GenericObjectType.objects.all(),
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
        model = models.GenericObject
        fields = ["name", "object_type", "metadata"]

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
