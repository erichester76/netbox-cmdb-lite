from django.urls import path
import views

urlpatterns = [
    # ObjectType URLs
    path("object-types/", views.ObjectTypeListView.as_view(), name="object_type_list"),
    path("object-types/add/", views.ObjectTypeEditView.as_view(), name="object_type_add"),
    path("object-types/<int:pk>/edit/", views.ObjectTypeEditView.as_view(), name="object_type_edit"),
    path("object-types/<int:pk>/delete/", views.ObjectTypeDeleteView.as_view(), name="object_type_delete"),

    # RelationshipType URLs
    path("relationship-types/", views.RelationshipTypeListView.as_view(), name="relationship_type_list"),
    path("relationship-types/add/", views.RelationshipTypeEditView.as_view(), name="relationship_type_add"),
    path("relationship-types/<int:pk>/edit/", views.RelationshipTypeEditView.as_view(), name="relationship_type_edit"),
    path("relationship-types/<int:pk>/delete/", views.RelationshipTypeDeleteView.as_view(), name="relationship_type_delete"),

    # GenericObject URLs
    path("generic-objects/", views.GenericObjectListView.as_view(), name="generic_object_list"),
    path("generic-objects/add/", views.GenericObjectEditView.as_view(), name="generic_object_add"),
    path("generic-objects/<int:pk>/edit/", views.GenericObjectEditView.as_view(), name="generic_object_edit"),
    path("generic-objects/<int:pk>/delete/", views.GenericObjectDeleteView.as_view(), name="generic_object_delete"),

    # GenericRelationship URLs
    path("generic-relationships/", views.GenericRelationshipListView.as_view(), name="generic_relationship_list"),
    path("generic-relationships/add/", views.GenericRelationshipEditView.as_view(), name="generic_relationship_add"),
    path("generic-relationships/<int:pk>/edit/", views.GenericRelationshipEditView.as_view(), name="generic_relationship_edit"),
    path("generic-relationships/<int:pk>/delete/", views.GenericRelationshipDeleteView.as_view(), name="generic_relationship_delete"),
]