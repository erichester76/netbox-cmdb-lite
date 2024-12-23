from netbox.api.routers import NetBoxRouter
from . import views

router = NetBoxRouter()
router.register('object-types', views.GenericObjectTypeViewSet)
router.register('generic-objects', views.GenericObjectViewSet)
router.register('relationship-types', views.RelationshipTypeViewSet)
router.register('generic-relationships', views.GenericRelationshipViewSet)

urlpatterns = router.urls
