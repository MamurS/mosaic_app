# apps/core/labels_registry.py
from __future__ import annotations

import json
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

from django.conf import settings
from django.utils import timezone

from apps.core.models import SystemSetting


# ---- helpers ---------------------------------------------------------------

def to_snake(name: str) -> str:
    """Normalize any label/header to a snake_case key."""
    import re

    if not isinstance(name, str):
        name = str(name or "")
    name = name.strip()
    name = re.sub(r"[^A-Za-z0-9]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name.lower().replace(" ", "_")


# A few common fallbacks in case nothing is loaded yet
DEFAULT_MAPPING: Dict[str, str] = {
    # Entities
    "legal_name": "Юридическое наименование",
    "trading_name": "Торговое наименование",
    "registration_number": "Регистрационный номер",
    "entity_type": "Тип организации",
    "country": "Страна",
    "industry": "Отрасль",
    "email": "Email",
    "phone": "Телефон",
    "mobile": "Мобильный телефон",
    "address_line1": "Адрес (строка 1)",
    "address_line2": "Адрес (строка 2)",
    "city": "Город",
    "state_province": "Область/Регион",
    "postal_code": "Почтовый индекс",
    "kyc_status": "Статус KYC",
    "aml_status": "Статус AML",
    "sanction_check_status": "Статус санкционной проверки",
    "credit_limit": "Кредитный лимит",
    "credit_terms_days": "Отсрочка платежа (дней)",

    # Finance
    "currency": "Валюта",
    "amount": "Сумма",
    "rate": "Ставка",
    "tax": "Налог",
}


# ---- registry --------------------------------------------------------------

@dataclass
class RegistryState:
    mapping: Dict[str, str] = field(default_factory=dict)
    source: str = "defaults"
    loaded_at: Optional[str] = None


class LabelRegistry:
    """
    Centralized label registry (server-side).
    Load order:
      1) SystemSetting key 'ui.labels' (JSON: {"mapping": {...}})
      2) File: insurance_project/assets/labels/labels.json
      3) DEFAULT_MAPPING (fallback)
    Exposes:
      - get(key), get_bulk(keys), all()
      - set_labels(mapping, source) -> persists into SystemSetting
      - refresh() -> re-read SystemSetting/file
    """

    SYSTEMSETTING_KEY = "ui.labels"
    FILE_REL_PATH = Path("insurance_project") / "assets" / "labels" / "labels.json"

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._state = RegistryState(mapping=DEFAULT_MAPPING.copy())

        # Load on startup
        try:
            self.refresh()
        except Exception:
            # if anything goes wrong, we keep DEFAULT_MAPPING
            pass

    # ---------- loaders ----------

    def _load_from_systemsetting(self) -> Optional[RegistryState]:
        ss = SystemSetting.objects.filter(key=self.SYSTEMSETTING_KEY).first()
        if not ss or not ss.value:
            return None
        try:
            data = json.loads(ss.value)
            mapping = data.get("mapping") or data  # accept plain dict or {"mapping": {...}}
            if not isinstance(mapping, dict):
                return None
            return RegistryState(mapping=mapping, source="systemsetting", loaded_at=timezone.now().isoformat())
        except Exception:
            return None

    def _load_from_file(self) -> Optional[RegistryState]:
        base_dir = Path(getattr(settings, "BASE_DIR", "."))
        file_path = base_dir / self.FILE_REL_PATH
        if not file_path.exists():
            return None
        try:
            with file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            mapping = data.get("mapping") or data
            if not isinstance(mapping, dict):
                return None
            return RegistryState(mapping=mapping, source=str(self.FILE_REL_PATH), loaded_at=timezone.now().isoformat())
        except Exception:
            return None

    # ---------- public API ----------

    def refresh(self) -> None:
        """Reload from SystemSetting or file; fallback to defaults."""
        with self._lock:
            state = self._load_from_systemsetting()
            if state is None:
                state = self._load_from_file()
            if state is None:
                state = RegistryState(mapping=DEFAULT_MAPPING.copy(), source="defaults", loaded_at=timezone.now().isoformat())
            self._state = state

    def get(self, key: str, default: Optional[str] = None) -> str:
        key = to_snake(key)
        with self._lock:
            return self._state.mapping.get(key, default if default is not None else key)

    def get_bulk(self, keys: Iterable[str]) -> Dict[str, str]:
        with self._lock:
            return {to_snake(k): self._state.mapping.get(to_snake(k), k) for k in keys}

    def all(self) -> Dict[str, str]:
        with self._lock:
            return dict(self._state.mapping)

    def set_labels(self, mapping: Dict[str, str], source: str = "manual") -> None:
        """
        Replace registry and persist under SystemSetting 'ui.labels'.
        Mapping keys are normalized to snake_case.
        """
        cleaned = {to_snake(k): str(v) for k, v in (mapping or {}).items()}
        payload = {"mapping": cleaned, "source": source, "updated_at": timezone.now().isoformat()}

        with self._lock:
            ss, _ = SystemSetting.objects.get_or_create(key=self.SYSTEMSETTING_KEY)
            ss.value = json.dumps(payload, ensure_ascii=False)
            ss.save(update_fields=["value", "updated_at"])
            self._state = RegistryState(mapping=cleaned, source="systemsetting", loaded_at=timezone.now().isoformat())


# module-level singleton
registry = LabelRegistry()

# convenience functions
def label(key: str, default: Optional[str] = None) -> str:
    return registry.get(key, default=default)


def labels(keys: Iterable[str]) -> Dict[str, str]:
    return registry.get_bulk(keys)


def all_labels() -> Dict[str, str]:
    return registry.all()
