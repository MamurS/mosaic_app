from rest_framework import filters, viewsets

from .models import (
    Entity,
    EntityContact,
    EntityFinancial,
    EntityRating,
    EntityRelationship,
    EntityRole,
)
from .serializers import (
    EntityFinancialSerializer,
    EntityRatingSerializer,
    EntityRelationshipSerializer,
    EntityRoleSerializer,
    EntityContactSerializer,
    EntitySerializer,
)


class BaseSearchFilterViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields: list[str] = []


class EntityViewSet(BaseSearchFilterViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    search_fields = ['legal_name', 'registration_number', 'tax_id']


class EntityRoleViewSet(BaseSearchFilterViewSet):
    queryset = EntityRole.objects.all()
    serializer_class = EntityRoleSerializer
    search_fields = ['name', 'entity__legal_name']


class EntityContactViewSet(BaseSearchFilterViewSet):
    queryset = EntityContact.objects.all()
    serializer_class = EntityContactSerializer
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'entity__legal_name']


class EntityRelationshipViewSet(BaseSearchFilterViewSet):
    queryset = EntityRelationship.objects.all()
    serializer_class = EntityRelationshipSerializer
    search_fields = ['relationship_type', 'from_entity__legal_name', 'to_entity__legal_name']


class EntityRatingViewSet(BaseSearchFilterViewSet):
    queryset = EntityRating.objects.all()
    serializer_class = EntityRatingSerializer
    search_fields = ['rating_agency', 'rating', 'entity__legal_name']


class EntityFinancialViewSet(BaseSearchFilterViewSet):
    queryset = EntityFinancial.objects.all()
    serializer_class = EntityFinancialSerializer
    search_fields = ['entity__legal_name', 'period']


