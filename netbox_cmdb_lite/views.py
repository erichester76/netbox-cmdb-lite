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
    model_form = forms.GenericObjectTypeForm
    
class GenericObjectDetailView(generic.ObjectView):
    queryset = models.GenericObjectType.objects.all()

class GenericObjectTypeDeleteView(generic.ObjectDeleteView):
    queryset = models.GenericObjectType.objects.all()

# RelationshipType Views
class RelationshipTypeListView(generic.ObjectListView):
    queryset = models.RelationshipType.objects.all()
    table = tables.RelationshipTypeTable

class RelationshipTypeEditView(generic.ObjectEditView):
    queryset = models.RelationshipType.objects.all()
    model_form = forms.RelationshipTypeForm

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
    model_form = forms.GenericObjectForm

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.metadata = form.cleaned_data.get("metadata", {})
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
    model_form = forms.RelationshipForm

class GenericRelationshipDeleteView(generic.ObjectDeleteView):
    queryset = models.GenericRelationship.objects.all()
