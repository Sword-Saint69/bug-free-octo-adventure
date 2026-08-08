import json
from pathlib import Path
from typing import Any

from app.core.config import settings


class ConfigService:
    """Runtime configuration persisted separately from the checked-in defaults."""

    @classmethod
    def config_path(cls) -> Path:
        if settings.RUNTIME_CONFIG_PATH:
            return Path(settings.RUNTIME_CONFIG_PATH)
        return Path(__file__).resolve().parents[2] / ".runtime-config.json"
    KEY_FIELDS = ("OPENAQ_API_KEY", "COINGECKO_API_KEY", "NASA_API_KEY")
    PUBLIC_FIELDS = ("DEFAULT_LATITUDE", "DEFAULT_LONGITUDE", "DEFAULT_COUNTRY_CODE")

    @classmethod
    def load(cls) -> None:
        config_path = cls.config_path()
        if not config_path.exists():
            return
        try:
            values = json.loads(config_path.read_text(encoding="utf-8"))
            for name in (*cls.KEY_FIELDS, *cls.PUBLIC_FIELDS):
                if name in values:
                    setattr(settings, name, values[name])
        except (OSError, ValueError, TypeError):
            return

    @staticmethod
    def mask(value: str) -> str:
        if not value:
            return ""
        if value == "DEMO_KEY":
            return value
        if len(value) <= 8:
            return "•" * len(value)
        return f"{value[:4]}{'•' * 8}{value[-4:]}"

    @classmethod
    def snapshot(cls) -> dict[str, Any]:
        return {
            "providers": {
                name: {
                    "configured": bool(getattr(settings, name, "")),
                    "masked_value": cls.mask(str(getattr(settings, name, ""))),
                }
                for name in cls.KEY_FIELDS
            },
            "defaults": {
                name: getattr(settings, name)
                for name in cls.PUBLIC_FIELDS
            },
        }

    @classmethod
    def update(cls, values: dict[str, Any]) -> dict[str, Any]:
        stored: dict[str, Any] = {}
        config_path = cls.config_path()
        if config_path.exists():
            try:
                stored = json.loads(config_path.read_text(encoding="utf-8"))
            except (OSError, ValueError, TypeError):
                stored = {}

        for name in (*cls.KEY_FIELDS, *cls.PUBLIC_FIELDS):
            value = values.get(name)
            if value is None:
                continue
            if name in cls.KEY_FIELDS and value == "":
                stored.pop(name, None)
                setattr(settings, name, "")
            else:
                stored[name] = value
                setattr(settings, name, value)

        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(stored, indent=2), encoding="utf-8")
        return cls.snapshot()
