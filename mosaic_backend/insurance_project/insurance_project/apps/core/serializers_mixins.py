# apps/core/serializers_mixins.py
from __future__ import annotations

from typing import Dict, Optional, Tuple

from django.db import models as dj_models
from rest_framework import serializers

from .labels_registry import registry, to_snake


def _model_field_verbose_help(model: Optional[type], source: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """
    Try to fetch (verbose_name, help_text) from a Django model field.
    Works when serializer field maps directly to a model field.
    """
    if not model or not source:
        return None, None
    try:
        field = model._meta.get_field(source)
    except Exception:
        return None, None
    # Convert Django's verbose_name (which can be lazy proxy) to str
    v = str(getattr(field, "verbose_name", "") or "") or None
    h = str(getattr(field, "help_text", "") or "") or None
    return v, h


class LabelledSerializerMixin:
    """
    Mixin that auto-applies labels from the central registry to DRF serializer fields.

    How it works:
      - For each serializer field:
          key := LABEL_MAP.get(field_name) or field.source or field_name
          key := to_snake(key)
          if LABEL_PREFIX is set: key := f"{LABEL_PREFIX}{key}"
      - field.label := registry.get(key)              (overwrites only if LABEL_OVERRIDE or missing)
      - field.help_text := registry.get(key + '__help') if defined in registry  (optional pattern)
      - If help not found in registry, falls back to model field's help_text.

    Customize per serializer:
      class MySerializer(LabelledSerializerMixin, serializers.ModelSerializer):
          LABEL_PREFIX = "entity."            # optional namespace in registry keys
          LABEL_OVERRIDE = True               # force override even if DRF/Model provides a label
          LABEL_MAP = {"credit_terms_days": "payment_terms_days"}  # remap specific keys

    Registry keys supported:
      - "<field_key>"            → label text
      - "<field_key>__help"      → help text (optional convention)
    """

    LABEL_PREFIX: Optional[str] = None
    LABEL_OVERRIDE: bool = False
    LABEL_MAP: Dict[str, str] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # type: ignore[misc]
        self._apply_labels()

    # ------------- internals -------------

    def _effective_key(self, field_name: str, field: serializers.Field) -> str:
        # Priority: explicit map → source → field name
        key = self.LABEL_MAP.get(field_name) or getattr(field, "source", None) or field_name
        key = to_snake(key)
        if self.LABEL_PREFIX:
            key = f"{self.LABEL_PREFIX}{key}"
        return key

    def _maybe_set_label(self, field: serializers.Field, key: str) -> None:
        new_label = registry.get(key, default=None)
        if not new_label:
            return

        current_label = getattr(field, "label", None)
        if self.LABEL_OVERRIDE or not current_label:
            field.label = new_label  # apply

    def _maybe_set_help(self, field: serializers.Field, key: str, model_cls: Optional[type], source: Optional[str]) -> None:
        # 1) convention: registry has "<key>__help"
        reg_help = registry.get(f"{key}__help", default=None)
        if reg_help:
            field.help_text = reg_help
            return

        # 2) if serializer maps to a model field, use its help_text
        if not getattr(field, "help_text", None) and model_cls and source:
            _, model_help = _model_field_verbose_help(model_cls, source)
            if model_help:
                field.help_text = model_help

    def _apply_labels(self) -> None:
        model_cls = getattr(getattr(self, "Meta", None), "model", None)
        for name, field in self.fields.items():
            key = self._effective_key(name, field)
            source = getattr(field, "source", None)

            self._maybe_set_label(field, key)
            self._maybe_set_help(field, key, model_cls, source)


class LabelledModelSerializer(LabelledSerializerMixin, serializers.ModelSerializer):
    """
    Drop-in replacement for DRF's ModelSerializer that auto-applies labels/help
    from the central registry. See LabelledSerializerMixin docs for options.
    """
    pass
