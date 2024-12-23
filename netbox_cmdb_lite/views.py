from netbox.views import NetBoxListView, NetBoxEditView, NetBoxDeleteView
import models
import tables
import forms

###################################
# Adjusted NetBox Plugin Views
###################################

# ObjectType Views
class ObjectTypeListView(NetBoxListView):
    queryset = models.ObjectType.objects.all()
    table = tables.ObjectTypeTable
    template_name = "object_types/object_type_list.html"

class ObjectTypeEditView(NetBoxEditView):
    queryset = models.ObjectType.objects.all()
    model_form = forms.ObjectTypeForm
    template_name = "object_types/object_type_edit.html"

class ObjectTypeDeleteView(NetBoxDeleteView):
    queryset = models.ObjectType.objects.all()
    template_name = "object_types/object_type_delete.html"

# RelationshipType Views
class RelationshipTypeListView(NetBoxListView):
    queryset = models.RelationshipType.objects.all()
    table = tables.RelationshipTypeTable
    template_name = "relationships/relationship_type_list.html"

class RelationshipTypeEditView(NetBoxEditView):
    queryset = models.RelationshipType.objects.all()
    model_form = forms.RelationshipTypeForm
    template_name = "relationships/relationship_type_edit.html"

class RelationshipTypeDeleteView(NetBoxDeleteView):
    queryset = models.RelationshipType.objects.all()
    template_name = "relationships/relationship_type_delete.html"

# GenericObject Views
class GenericObjectListView(NetBoxListView):
    queryset = models.GenericObject.objects.all()
    table = tables.GenericObjectTable
    template_name = "generic_objects/generic_object_list.html"

class GenericObjectEditView(NetBoxEditView):
    queryset = models.GenericObject.objects.all()
    model_form = forms.GenericObjectForm
    template_name = "generic_objects/generic_object_edit.html"

class GenericObjectDeleteView(NetBoxDeleteView):
    queryset = models.GenericObject.objects.all()
    template_name = "generic_objects/generic_object_delete.html"

# GenericRelationship Views
class GenericRelationshipListView(NetBoxListView):
    queryset = models.GenericRelationship.objects.all()
    table = tables.GenericRelationshipTable
    template_name = "relationships/generic_relationship_list.html"

class GenericRelationshipEditView(NetBoxEditView):
    queryset = models.GenericRelationship.objects.all()
    model_form = forms.RelationshipForm
    template_name = "relationships/generic_relationship_edit.html"

class GenericRelationshipDeleteView(NetBoxDeleteView):
    queryset = models.GenericRelationship.objects.all()
    template_name = "relationships/generic_relationship_delete.html"