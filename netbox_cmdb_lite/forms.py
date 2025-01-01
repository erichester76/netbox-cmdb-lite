from django.contrib.contenttypes.models import ContentType
from django import forms
from django.forms import formset_factory
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import DynamicModelChoiceField, DynamicModelMultipleChoiceField, JSONField
from . import models
import json


class CategoryForm(NetBoxModelForm):
    class Meta:
        model = models.Category
        fields = ["name", "description"]

class GenericObjectTypeForm(NetBoxModelForm):
    category = DynamicModelChoiceField(
        queryset=models.Category.objects.all(),
        label="Category",
        required=False,
        help_text="Select a category for this object type",
    )


    class Meta:
        model = models.GenericObjectType
        fields = ['name', 'category']
                        
class ObjectTypeAttributeForm(forms.Form):
    name = forms.CharField(label="Field Name", required=True)
    type = forms.ChoiceField(
        choices=[
            ("string", "String"),
            ("integer", "Integer"),
            ("boolean", "Boolean"),
            ("multi-choice", "Multi-Choice"),
            ("foreign-key", "Foreign Key"),
        ],
        required=True,
    )
    options = forms.CharField(label="Options", required=False)
    reference = forms.CharField(label="Reference", required=False)


class ObjectTypeRelationshipForm(forms.Form):
    relationship_type = DynamicModelChoiceField(
        queryset=models.RelationshipType.objects.all(),
        label="Relationship Type",
        required=True,
    )
    allowed_types = forms.MultipleChoiceField(
        choices=[
            (f"{ct.pk}", f"{ct.app_label}.{ct.model}")
            for ct in ContentType.objects.filter(app_label__in=['dcim', 'virtualization', 'ipam', 'tenancy'])
        ],
        label="Allowed Object Types",
        required=False,
    )

ObjectTypeAttributeFormSet = formset_factory(ObjectTypeAttributeForm, extra=0, can_delete=True)
ObjectTypeRelationshipFormSet = formset_factory(ObjectTypeRelationshipForm, extra=0, can_delete=True)

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
