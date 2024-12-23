from django.urls import path
from . import views

urlpatterns = [
    # GenericObjectType URLs
    path("generic-object-types/", views.GenericObjectTypeListView.as_view(), name="generic_object_type_list"),
    path("generic-object-types/add/", views.GenericObjectTypeEditView.as_view(), name="generic_object_type_add"),
    path("generic-object-types/<int:pk>/edit/", views.GenericObjectTypeEditView.as_view(), name="generic_object_type_edit"),
    path("generic-object-types/<int:pk>/", views.GenericObjectDetailView.as_view(), name="generic_object_type"),
    path("generic-object-types/<int:pk>/delete/", views.GenericObjectTypeDeleteView.as_view(), name="generic_object_type_delete"),
    path("generic-object-types/<int:pk>/attributes/", views.object_type_attributes, name="generic_object_type_attributes"),

    # RelationshipType URLs
    path("relationship-types/", views.RelationshipTypeListView.as_view(), name="relationship_type_list"),
    path("relationship-types/add/", views.RelationshipTypeEditView.as_view(), name="relationship_type_add"),
    path("relationship-types/<int:pk>/", views.RelationshipTypeDetailView.as_view(), name="relationship_type"),
    path("relationship-types/<int:pk>/edit/", views.RelationshipTypeEditView.as_view(), name="relationship_type_edit"),
    path("relationship-types/<int:pk>/delete/", views.RelationshipTypeDeleteView.as_view(), name="relationship_type_delete"),

    # GenericObject URLs
    path("generic-objects/", views.GenericObjectListView.as_view(), name="generic_object_list"),
    path("generic-objects/add/", views.GenericObjectEditView.as_view(), name="generic_object_add"),
    path("generic-objects/<int:pk>/", views.GenericObjectDetailView.as_view(), name="generic_object"),
    path("generic-objects/<int:pk>/edit/", views.GenericObjectEditView.as_view(), name="generic_object_edit"),
    path("generic-objects/<int:pk>/delete/", views.GenericObjectDeleteView.as_view(), name="generic_object_delete"),

    # GenericRelationship URLs
    path("generic-relationships/", views.GenericRelationshipListView.as_view(), name="generic_relationship_list"),
    path("generic-relationships/add/", views.GenericRelationshipEditView.as_view(), name="generic_relationship_add"),
    path("generic-relationships/<int:pk>/", views.GenericRelationshipDetailView.as_view(), name="generic_relationship"),
    path("generic-relationships/<int:pk>/edit/", views.GenericRelationshipEditView.as_view(), name="generic_relationship_edit"),
    path("generic-relationships/<int:pk>/delete/", views.GenericRelationshipDeleteView.as_view(), name="generic_relationship_delete"),
]