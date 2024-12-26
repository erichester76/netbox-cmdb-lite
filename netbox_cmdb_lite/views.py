from netbox.views import generic
from . import models
from . import tables
from . import forms
from django.http import JsonResponse
import json

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
        print("Attributes before saving:", instance.attributes)  # Debugging output
        instance.save()
        return super().form_valid(form)

class GenericObjectTypeDetailView(generic.ObjectView):
    queryset = models.GenericObjectType.objects.all()
    
    def get_extra_context(self, request, instance):
        
        return {
            'fields': [
                ('Name', instance.name),
                ('Created', instance.created),
                ('Last Updated', instance.last_updated),
            ],
            'attributes': instance.attributes
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
def object_type_attributes(request, pk):
    object_type = models.GenericObjectType.objects.filter(pk=pk).first()
    if not object_type:
        return JsonResponse({"error": "ObjectType not found."}, status=404)
    attributes = object_type.attributes or {}
    return JsonResponse({"attributes": attributes})

# GenericObject Views
class GenericObjectListView(generic.ObjectListView):
    queryset = models.GenericObject.objects.all()
    table = tables.GenericObjectTable

class GenericObjectDetailView(generic.ObjectView):
    queryset = models.GenericObject.objects.all()
    template_name = "netbox_cmdb_lite/genericobject_detail.html"

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
    form = models.GenericObjectForm
    template_name = "netbox_cmdb_lite/genericobject_edit.html"

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        instance = kwargs.get('instance') or self.get_object()
        if instance and instance.object_type:
            form._add_dynamic_fields(instance.object_type)
        return form

    def form_valid(self, form):
        instance = form.save(commit=False)
        # Save metadata
        metadata = {}
        for field in form.fields:
            if field in instance.object_type.attributes:
                metadata[field] = form.cleaned_data[field]
        instance.metadata = metadata
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
