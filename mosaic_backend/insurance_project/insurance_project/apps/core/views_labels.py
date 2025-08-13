# apps/core/views_labels.py
from __future__ import annotations

from typing import Dict

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from apps.core.labels_registry import registry, to_snake


class LabelsView(APIView):
    """
    GET /api/v1/core/labels/
      - returns the label mapping
      - query:
          keys: comma-separated keys to filter (e.g., ?keys=legal_name,registration_number)
          search: substring on keys or labels (e.g., ?search=credit)
          limit: int to truncate
    PUT /api/v1/core/labels/
      - (admin only) replace OR merge labels mapping in the registry (persisted in SystemSetting)
      - body: {"mapping": {...}, "merge": true|false}
    PATCH /api/v1/core/labels/
      - (admin only) always merge into existing mapping
      - body: {"mapping": {...}}
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # GET -> any authenticated user; PUT/PATCH -> admin only
        if self.request.method in ("PUT", "PATCH"):
            return [IsAdminUser()]
        return [IsAuthenticated()]

    # ---------- READ ----------
    def get(self, request):
        mapping = registry.all()

        keys_param = request.query_params.get("keys")
        if keys_param:
            keys = [to_snake(k) for k in keys_param.split(",")]
            mapping = {k: mapping.get(k, k) for k in keys}

        search = request.query_params.get("search")
        if search:
            s = search.lower()
            mapping = {k: v for k, v in mapping.items() if s in k.lower() or s in str(v).lower()}

        limit = request.query_params.get("limit")
        if limit:
            try:
                n = max(0, int(limit))
                mapping = dict(list(mapping.items())[:n])
            except Exception:
                pass

        return Response({"labels": mapping})

    # ---------- REPLACE / MERGE ----------
    def put(self, request):
        data = request.data or {}
        incoming = data.get("mapping") or {}
        if not isinstance(incoming, dict):
            return Response({"detail": "mapping must be an object"}, status=status.HTTP_400_BAD_REQUEST)

        merge = bool(data.get("merge", False))
        normalized: Dict[str, str] = {to_snake(k): str(v) for k, v in incoming.items()}

        if merge:
            current = registry.all()
            current.update(normalized)
            registry.set_labels(current, source="admin_merge_put")
        else:
            registry.set_labels(normalized, source="admin_replace_put")

        return Response({"labels": registry.all(), "mode": "merge" if merge else "replace"}, status=status.HTTP_200_OK)

    # ---------- MERGE (partial) ----------
    def patch(self, request):
        data = request.data or {}
        incoming = data.get("mapping") or {}
        if not isinstance(incoming, dict):
            return Response({"detail": "mapping must be an object"}, status=status.HTTP_400_BAD_REQUEST)

        current = registry.all()
        current.update({to_snake(k): str(v) for k, v in incoming.items()})
        registry.set_labels(current, source="admin_merge_patch")

        return Response({"labels": registry.all(), "mode": "merge"}, status=status.HTTP_200_OK)
