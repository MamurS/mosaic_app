from __future__ import annotations

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.core.models import Currency, Country, Industry, SystemSetting, AuditLog
from apps.core.serializers_mixins import LabelledModelSerializer

User = get_user_model()


class UserSerializer(LabelledModelSerializer):
    class Meta:
        model = User
        # password and permissions are intentionally excluded here
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "org_unit",
            "phone",
            "locale",
            "timezone",
            "uw_currency",
            "uw_limit",
            "claims_currency",
            "claims_limit",
            "can_underwrite",
            "can_handle_claims",
            "can_approve_payments",
            "last_login",
            "date_joined",
        ]
        read_only_fields = ["id", "last_login", "date_joined"]


class CurrencySerializer(LabelledModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "code", "name", "symbol", "rate_to_base", "is_default"]
        read_only_fields = ["id"]


class CountrySerializer(LabelledModelSerializer):
    class Meta:
        model = Country
        fields = [
            "id",
            "iso2",
            "iso3",
            "name_en",
            "name_local",
            "dialing_code",
            "is_sanctioned",
        ]
        read_only_fields = ["id"]


class IndustrySerializer(LabelledModelSerializer):
    # Example of mapping override (if needed):
    # LABEL_MAP = {"name": "industry_name"}

    class Meta:
        model = Industry
        fields = ["id", "code", "name", "parent"]
        read_only_fields = ["id"]


class SystemSettingSerializer(LabelledModelSerializer):
    class Meta:
        model = SystemSetting
        fields = ["id", "key", "value", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class AuditLogSerializer(LabelledModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            "id",
            "action",
            "actor",
            "object_id",
            "object_type",
            "timestamp",
            "changes",
            "ip_address",
            "user_agent",
        ]
        read_only_fields = ["id", "timestamp"]
