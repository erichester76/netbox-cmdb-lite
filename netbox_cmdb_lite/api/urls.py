from netbox.api.routers import NetBoxRouter
from .views import (
    ObjectTypeViewSet,
    GenericObjectViewSet,
    RelationshipTypeViewSet,
    GenericRelationshipViewSet,
)

router = NetBoxRouter()
router.register('object-types', ObjectTypeViewSet)
router.register('generic-objects', GenericObjectViewSet)
router.register('relationship-types', RelationshipTypeViewSet)
router.register('generic-relationships', GenericRelationshipViewSet)

urlpatterns = router.urls
