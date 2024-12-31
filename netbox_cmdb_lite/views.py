from netbox.views import generic
from . import models
from . import tables
from . import forms
from django.contrib.contenttypes.models import ContentType
import json

class CategoryListView(generic.ObjectListView):
    queryset = models.Category.objects.all()
    table = "CategoryTable"

class CategoryEditView(generic.ObjectEditView):
    queryset = models.Category.objects.all()
    model_form = forms.CategoryForm

class CategoryDeleteView(generic.ObjectDeleteView):
    queryset = models.Category.objects.all()

class CategoryDetailView(generic.ObjectView):
    queryset = models.Category.objects.all()


# GenericObjectType Views
class GenericObjectTypeListView(generic.ObjectListView):
    queryset = models.GenericObjectType.objects.all()
    table = tables.GenericObjectTypeTable

class GenericObjectTypeEditView(generic.ObjectEditView):
    queryset = models.GenericObjectType.objects.all()
    form = forms.GenericObjectTypeForm
    template_name = "generic/object_edit.html"

    def get_extra_context(self, request, instance):
        # Initialize formsets for attributes and relationships
        attribute_formset = forms.ObjectTypeAttributeFormSet(
            data=request.POST if request.method == "POST" else None,
            prefix="attributes",
            initial=instance.attributes if instance else [],
        )
        relationship_formset = forms.ObjectTypeRelationshipFormSet(
            data=request.POST if request.method == "POST" else None,
            prefix="relationships",
            initial=instance.relationships if instance else [],
        )

        return {
            "attribute_formset": attribute_formset,
            "relationship_formset": relationship_formset,
        }

    def post(self, request, *args, **kwargs):
        """Handle POST requests for saving attributes and relationships."""
        instance = self.get_object()
        form = self.get_form()

        # Initialize formsets
        attribute_formset = forms.ObjectTypeAttributeFormSet(request.POST, prefix="attributes")
        relationship_formset = forms.ObjectTypeRelationshipFormSet(request.POST, prefix="relationships")

        if form.is_valid() and attribute_formset.is_valid() and relationship_formset.is_valid():
            instance = form.save(commit=False)

            # Save attributes
            attributes = [
                attr.cleaned_data for attr in attribute_formset if not attr.cleaned_data.get("DELETE", False)
            ]
            instance.attributes = attributes

            # Save relationships
            relationships = [
                {
                    "relationship_type": str(rel.cleaned_data["relationship_type"].pk),
                    "allowed_types": [str(ct.pk) for ct in rel.cleaned_data["allowed_types"]],
                }
                for rel in relationship_formset if not rel.cleaned_data.get("DELETE", False)
            ]
            instance.relationships = relationships

            # Save the instance
            instance.save()
            return self.form_valid(form)

        return self.form_invalid(form)


class GenericObjectTypeDetailView(generic.ObjectView):
    queryset = models.GenericObjectType.objects.all()
    
    def get_extra_context(self, request, instance):
        relationships = instance.relationships or []

        relationship_type_map = {str(rt.pk): rt.name for rt in models.RelationshipType.objects.all()}
        generic_object_type_map = {f"cmdb:{obj.pk}": obj.name for obj in models.GenericObjectType.objects.all()}
        netbox_content_type_map = {f"netbox:{ct.pk}": f"{ct.app_label}.{ct.model}" for ct in ContentType.objects.filter(
                                    app_label__in=['dcim', 'virtualization', 'ipam', 'tenancy', 'extras'])}
        allowed_type_map = {**generic_object_type_map, **netbox_content_type_map}

        # Replace the relationship type ID with its name in the relationships list
        for relationship in relationships:
            relationship['relationship_type'] = relationship_type_map.get(str(relationship['relationship_type']), "Unknown")
            relationship["allowed_types"] = [allowed_type_map.get(allowed_type, "Unknown") for allowed_type in relationship["allowed_types"]]
       
        return {
            'fields': [
                ('Name', instance.name),
                ('Created', instance.created),
                ('Category', instance.category),
                ('Last Updated', instance.last_updated),
            ],
            'attributes': instance.attributes,
            'relationships': instance.relationships
        }
           
class GenericObjectTypeDeleteView(generic.ObjectDeleteView):
    queryset = models.GenericObjectType.objects.all()

# RelationshipType Views
class RelationshipTypeListView(generic.ObjectListView):
    queryset = models.RelationshipType.objects.all()
    table = tables.RelationshipTypeTable

class RelationshipTypeEditView(generic.ObjectEditView):
    queryset = models.RelationshipType.objects.all()
    form = forms.RelationshipTypeForm

    def form_valid(self, form):
        instance = form.save(commit=False)

        # Ensure `attributes` is saved as JSON (not stringified JSON)
        if isinstance(instance.attributes, str):
            instance.attributes = json.loads(instance.attributes)

        instance.save()
        return super().form_valid(form)
    
class RelationshipTypeDetailView(generic.ObjectView):
    queryset = models.RelationshipType.objects.all()

class RelationshipTypeDeleteView(generic.ObjectDeleteView):
    queryset = models.RelationshipType.objects.all()

class GenericObjectListView(generic.ObjectListView):
    queryset = models.GenericObject.objects.all()
    table = tables.GenericObjectTable

class GenericObjectDetailView(generic.ObjectView):
    queryset = models.GenericObject.objects.all()

    def get_extra_context(self, request, instance):
        attributes = []
        if instance.object_type and instance.metadata:
            for attr in instance.object_type.attributes:
                name = attr["name"]
                value = instance.metadata.get(name, "N/A")
                attributes.append({"name": name, "type": attr["type"], "value": value})

        return {
            "fields": [
                ("Name", instance.name),
                ("Object Type", instance.object_type.name),
                ("Created", instance.created),
                ("Last Updated", instance.last_updated),
            ],
            "attributes": attributes
        }


class GenericObjectEditView(generic.ObjectEditView):
    queryset = models.GenericObject.objects.all()
    form = forms.GenericObjectForm
    template_name = "netbox_cmdb_lite/genericobject_edit.html"

    def form_valid(self, form):
        # Save the object but include metadata
        instance = form.save(commit=False)
        metadata = form.cleaned_data.get("metadata", {})
        instance.metadata = metadata  # Save metadata to the model
        instance.save()
        return super().form_valid(form)



class GenericObjectDeleteView(generic.ObjectDeleteView):
    queryset = models.GenericObject.objects.all()

# GenericRelationship Views
class GenericRelationshipListView(generic.ObjectListView):
    queryset = models.GenericRelationship.objects.all()
    table = tables.GenericRelationshipTable

class GenericRelationshipDetailView(generic.ObjectView):
    queryset = models.GenericRelationship.objects.all()

class GenericRelationshipEditView(generic.ObjectEditView):
    queryset = models.GenericRelationship.objects.all()
    form = forms.RelationshipForm

class GenericRelationshipDeleteView(generic.ObjectDeleteView):
    queryset = models.GenericRelationship.objects.all()
