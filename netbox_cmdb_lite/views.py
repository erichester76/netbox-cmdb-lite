from netbox.views import generic
from . import models
from . import tables
from . import forms
from django.http import JsonResponse
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
    template_name = "netbox_cmdb_lite/genericobjecttype_edit.html"
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        return super().form_valid(form)

class GenericObjectTypeDetailView(generic.ObjectView):
    queryset = models.GenericObjectType.objects.all()
    
    def get_extra_context(self, request, instance):
        relationships = instance.relationships or []

        # Fetch all RelationshipType objects to map ID to name
        relationship_type_map = {
            str(rt.pk): rt.name for rt in models.RelationshipType.objects.all()
        }

        # Replace the relationship type ID with its name in the relationships list
        for relationship in relationships:
            relationship['relationship_types'] = relationship_type_map.get(str(relationship['relationship_types']), "Unknown")

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
            import json
            instance.attributes = json.loads(instance.attributes)

        instance.save()
        return super().form_valid(form)
    
class RelationshipTypeDetailView(generic.ObjectView):
    queryset = models.RelationshipType.objects.all()

class RelationshipTypeDeleteView(generic.ObjectDeleteView):
    queryset = models.RelationshipType.objects.all()

# ObjectType Attributes API
def get_object_type_attributes(request, pk):
    try:
        object_type = models.GenericObjectType.objects.get(pk=pk)
        return JsonResponse({"attributes": object_type.attributes}, safe=False)
    except models.GenericObjectType.DoesNotExist:
        return JsonResponse({"error": "Object type not found"}, status=404)

# GenericObject Views
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
