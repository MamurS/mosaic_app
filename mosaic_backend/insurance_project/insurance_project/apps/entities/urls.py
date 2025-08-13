from rest_framework.routers import DefaultRouter

from .views import (
    EntityContactViewSet,
    EntityFinancialViewSet,
    EntityRatingViewSet,
    EntityRelationshipViewSet,
    EntityRoleViewSet,
    EntityViewSet,
)

router = DefaultRouter()
router.register(r'entities', EntityViewSet, basename='entities')
router.register(r'entity-roles', EntityRoleViewSet, basename='entity-roles')
router.register(r'entity-contacts', EntityContactViewSet, basename='entity-contacts')
router.register(r'entity-relationships', EntityRelationshipViewSet, basename='entity-relationships')
router.register(r'entity-ratings', EntityRatingViewSet, basename='entity-ratings')
router.register(r'entity-financials', EntityFinancialViewSet, basename='entity-financials')

urlpatterns = router.urls


