from netbox.views import generic
from . import models
from . import tables
from . import forms
from django.http import JsonResponse

###################################
# Adjusted generic.Object Plugin Views
###################################

# GenericObjectType Views
class GenericObjectTypeListView(generic.ObjectListView):
    queryset = models.GenericObjectType.objects.all()
    table = tables.GenericObjectTypeTable

class GenericObjectTypeEditView(generic.ObjectEditView):
    queryset = models.GenericObjectType.objects.all()
    form = forms.GenericObjectTypeForm
    template_name = "netbox_cmdb_lite/generic_object_type_edit.html"  


class GenericObjectTypeDetailView(generic.ObjectDetailView):
    queryset = models.GenericObjectType.objects.all()
    template_name = "netbox/object_detail.html"  

    def get_extra_context(self, request, instance):
        """
        Preprocess attributes and related objects for display in the detail view.
        """
        # Expand the attributes field
        attributes = instance.attributes or []
        expanded_fields = []
        for attribute in attributes:
            field_data = {
                'name': attribute.get('name'),
                'type': attribute.get('type'),
                'options': ', '.join(attribute.get('options', [])) if attribute.get('type') == 'multi-choice' else None,
                'reference': attribute.get('reference') if attribute.get('type') == 'foreign-key' else None,
            }
            expanded_fields.append(field_data)

        # Fetch related objects
        related_objects = models.GenericObject.objects.filter(object_type=instance)

        # Prepare NetBox-compatible fields
        fields = [
            ('Name', instance.name),
            ('Created', instance.created),
            ('Last Updated', instance.last_updated),
            ('Attributes', expanded_fields),
        ]

        return {
            'fields': fields,
            'related_objects': {
                'name': 'Related Objects',
                'objects': related_objects,
                'table': 'GenericObjectTable',
                'edit_url_name': 'plugins:netbox_cmdb_lite:generic_object_edit',
            },
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

class GenericObjectEditView(generic.ObjectEditView):
    queryset = models.GenericObject.objects.all()
    form = forms.GenericObjectForm

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
