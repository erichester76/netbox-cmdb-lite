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
    template_name = "object_types/object_type_list.html"

class GenericObjectTypeEditView(generic.ObjectEditView):
    queryset = models.GenericObjectType.objects.all()
    model_form = forms.GenericObjectTypeForm
    template_name = "object_types/object_type_edit.html"

class GenericObjectTypeDeleteView(generic.ObjectDeleteView):
    queryset = models.GenericObjectType.objects.all()
    template_name = "object_types/object_type_delete.html"

# RelationshipType Views
class RelationshipTypeListView(generic.ObjectListView):
    queryset = models.RelationshipType.objects.all()
    table = tables.RelationshipTypeTable
    template_name = "relationships/relationship_type_list.html"

class RelationshipTypeEditView(generic.ObjectEditView):
    queryset = models.RelationshipType.objects.all()
    model_form = forms.RelationshipTypeForm
    template_name = "relationships/relationship_type_edit.html"

class RelationshipTypeDeleteView(generic.ObjectDeleteView):
    queryset = models.RelationshipType.objects.all()
    template_name = "relationships/relationship_type_delete.html"

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
    template_name = "generic_objects/generic_object_list.html"

class GenericObjectEditView(generic.ObjectEditView):
    queryset = models.GenericObject.objects.all()
    model_form = forms.GenericObjectForm
    template_name = "generic_objects/generic_object_edit.html"

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.metadata = form.cleaned_data.get("metadata", {})
        instance.save()
        return super().form_valid(form)

class GenericObjectDeleteView(generic.ObjectDeleteView):
    queryset = models.GenericObject.objects.all()
    template_name = "generic_objects/generic_object_delete.html"

# GenericRelationship Views
class GenericRelationshipListView(generic.ObjectListView):
    queryset = models.GenericRelationship.objects.all()
    table = tables.GenericRelationshipTable
    template_name = "relationships/generic_relationship_list.html"

class GenericRelationshipEditView(generic.ObjectEditView):
    queryset = models.GenericRelationship.objects.all()
    model_form = forms.RelationshipForm
    template_name = "relationships/generic_relationship_edit.html"

class GenericRelationshipDeleteView(generic.ObjectDeleteView):
    queryset = models.GenericRelationship.objects.all()
    template_name = "relationships/generic_relationship_delete.html"