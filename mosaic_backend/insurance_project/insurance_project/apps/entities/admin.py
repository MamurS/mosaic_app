from django.contrib import admin

from .models.entities import (
    Entity,
    EntityContact,
    EntityFinancial,
    EntityRating,
    EntityRelationship,
    EntityRole,
)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = (
        'legal_name',
        'registration_number',
        'tax_id',
        'country',
        'industry',
        'is_active',
    )
    search_fields = ('legal_name', 'registration_number', 'tax_id')
    list_filter = ('country', 'industry', 'is_active')


@admin.register(EntityRole)
class EntityRoleAdmin(admin.ModelAdmin):
    list_display = ('entity', 'name')
    search_fields = ('entity__legal_name', 'name')


@admin.register(EntityContact)
class EntityContactAdmin(admin.ModelAdmin):
    list_display = ('entity', 'first_name', 'last_name', 'email', 'phone')
    search_fields = ('entity__legal_name', 'first_name', 'last_name', 'email', 'phone')


@admin.register(EntityRelationship)
class EntityRelationshipAdmin(admin.ModelAdmin):
    list_display = ('from_entity', 'relationship_type', 'to_entity')
    search_fields = (
        'from_entity__legal_name',
        'to_entity__legal_name',
        'relationship_type',
    )


@admin.register(EntityRating)
class EntityRatingAdmin(admin.ModelAdmin):
    list_display = ('entity', 'rating_agency', 'rating', 'effective_date')
    search_fields = ('entity__legal_name', 'rating_agency', 'rating')


@admin.register(EntityFinancial)
class EntityFinancialAdmin(admin.ModelAdmin):
    list_display = ('entity', 'period', 'currency', 'revenue', 'net_income')
    search_fields = ('entity__legal_name', 'period')
    list_filter = ('currency',)


