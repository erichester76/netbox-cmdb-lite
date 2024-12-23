from netbox.views import generic
from . import models
from . import tables
from . import forms

###################################
# Adjusted generic.Object Plugin Views
###################################

# ObjectType Views
class ObjectTypeListView(generic.ObjectListView):
    queryset = models.ObjectType.objects.all()
    table = tables.ObjectTypeTable
    template_name = "object_types/object_type_list.html"

class ObjectTypeEditView(generic.ObjectEditView):
    queryset = models.ObjectType.objects.all()
    model_form = forms.ObjectTypeForm
    template_name = "object_types/object_type_edit.html"

class ObjectTypeDeleteView(generic.ObjectDeleteView):
    queryset = models.ObjectType.objects.all()
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

# GenericObject Views
class GenericObjectListView(generic.ObjectListView):
    queryset = models.GenericObject.objects.all()
    table = tables.GenericObjectTable
    template_name = "generic_objects/generic_object_list.html"

class GenericObjectEditView(generic.ObjectEditView):
    queryset = models.GenericObject.objects.all()
    model_form = forms.GenericObjectForm
    template_name = "generic_objects/generic_object_edit.html"

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