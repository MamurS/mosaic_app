from rest_framework import serializers

from .models.entities import (
    Entity,
    EntityContact,
    EntityFinancial,
    EntityRating,
    EntityRelationship,
    EntityRole,
)


class EntityContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityContact
        fields = '__all__'


class EntityRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityRole
        fields = '__all__'


class EntitySerializer(serializers.ModelSerializer):
    contacts = EntityContactSerializer(many=True, read_only=True)
    roles = EntityRoleSerializer(many=True, read_only=True)

    class Meta:
        model = Entity
        fields = '__all__'


class EntityRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityRelationship
        fields = '__all__'


class EntityRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityRating
        fields = '__all__'


class EntityFinancialSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntityFinancial
        fields = '__all__'


