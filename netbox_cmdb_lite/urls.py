from django.urls import path
from . import views
from . import models
from netbox.views.generic import ObjectChangeLogView

urlpatterns = [

    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/add/", views.CategoryEditView.as_view(), name="category_add"),
    path("categories/<int:pk>/edit/", views.CategoryEditView.as_view(), name="category_edit"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category_delete"),
    path(
        "categories/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="categories_changelog",
        kwargs={"model": models.Category},
    ),

    # GenericObjectType URLs
    path("generic-object-types/", views.GenericObjectTypeListView.as_view(), name="genericobjecttype_list"),
    path("generic-object-types/add/", views.GenericObjectTypeEditView.as_view(), name="genericobjecttype_add"),
    path("generic-object-types/<int:pk>/edit/", views.GenericObjectTypeEditView.as_view(), name="genericobjecttype_edit"),
    path("generic-object-types/<int:pk>/", views.GenericObjectTypeDetailView.as_view(), name="genericobjecttype"),
    path("generic-object-types/<int:pk>/delete/", views.GenericObjectTypeDeleteView.as_view(), name="genericobjecttype_delete"),
    path(
        "generic-object-types/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="genericobjecttype_changelog",
        kwargs={"model": models.GenericObjectType},
    ),
    
    # GenericObject URLs
    path("generic-objects/", views.GenericObjectListView.as_view(), name="genericobject_list"),
    path("generic-objects/add/", views.GenericObjectEditView.as_view(), name="genericobject_add"),
    path("generic-objects/<int:pk>/", views.GenericObjectDetailView.as_view(), name="genericobject"),
    path("generic-objects/<int:pk>/edit/", views.GenericObjectEditView.as_view(), name="genericobject_edit"),
    path("generic-objects/<int:pk>/delete/", views.GenericObjectDeleteView.as_view(), name="genericobject_delete"),
    path(
        "generic-objects/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="genericobject_changelog",
        kwargs={"model": models.GenericObject},
    ),
    # RelationshipType URLs
    path("relationship-types/", views.RelationshipTypeListView.as_view(), name="relationshiptype_list"),
    path("relationship-types/add/", views.RelationshipTypeEditView.as_view(), name="relationshiptype_add"),
    path("relationship-types/<int:pk>/", views.RelationshipTypeDetailView.as_view(), name="relationshiptype"),
    path("relationship-types/<int:pk>/edit/", views.RelationshipTypeEditView.as_view(), name="relationshiptype_edit"),
    path("relationship-types/<int:pk>/delete/", views.RelationshipTypeDeleteView.as_view(), name="relationshiptype_delete"),
    path(
        "relationship-types/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="relationshiptype_changelog",
        kwargs={"model": models.RelationshipType},
    ),
    # GenericRelationship URLs
    path("generic-relationships/", views.GenericRelationshipListView.as_view(), name="genericrelationship_list"),
    path("generic-relationships/add/", views.GenericRelationshipEditView.as_view(), name="genericrelationship_add"),
    path("generic-relationships/<int:pk>/", views.GenericRelationshipDetailView.as_view(), name="genericrelationship"),
    path("generic-relationships/<int:pk>/edit/", views.GenericRelationshipEditView.as_view(), name="genericrelationship_edit"),
    path("generic-relationships/<int:pk>/delete/", views.GenericRelationshipDeleteView.as_view(), name="genericrelationship_delete"),
    path(
        "generic-relationships/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="genericrelationship_changelog",
        kwargs={"model": models.GenericRelationship},
    ),
]