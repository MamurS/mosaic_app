from __future__ import annotations

from rest_framework import serializers

from apps.core.serializers_mixins import LabelledModelSerializer
from .models import (
    Entity,
    EntityRole,
    EntityContact,
    EntityRelationship,
    EntityRating,
    EntityFinancial,
)


# ---- leaf serializers -------------------------------------------------------

class EntityContactSerializer(LabelledModelSerializer):
    class Meta:
        model = EntityContact
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]


class EntityRoleSerializer(LabelledModelSerializer):
    class Meta:
        model = EntityRole
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]


class EntityRelationshipSerializer(LabelledModelSerializer):
    class Meta:
        model = EntityRelationship
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]


class EntityRatingSerializer(LabelledModelSerializer):
    class Meta:
        model = EntityRating
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]


class EntityFinancialSerializer(LabelledModelSerializer):
    class Meta:
        model = EntityFinancial
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]


# ---- entity (root) ----------------------------------------------------------

class EntitySerializer(LabelledModelSerializer):
    """
    Main Entity serializer.
    - Includes computed fields: display_name, is_compliant
    - Nests contacts & roles by default (read-only lists)
    - Ratings/financials can be heavy; exposed as optional nested lists via separate serializer below
    """

    display_name = serializers.CharField(read_only=True)
    is_compliant = serializers.BooleanField(read_only=True)

    contacts = EntityContactSerializer(many=True, read_only=True)
    roles = EntityRoleSerializer(many=True, read_only=True)

    class Meta:
        model = Entity
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "created_by", "updated_by"]


class EntityWithDetailsSerializer(EntitySerializer):
    """
    Extended Entity serializer including heavier nested datasets.
    Use this for detail views where you need full picture.
    """

    ratings = EntityRatingSerializer(many=True, read_only=True)
    financials = EntityFinancialSerializer(many=True, read_only=True)

    class Meta(EntitySerializer.Meta):
        fields = EntitySerializer.Meta.fields + ("ratings", "financials",)
