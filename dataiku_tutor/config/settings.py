"""Configuration access layer backed by YAML settings."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class Settings:
    """Loads and exposes typed configuration sections."""

    def __init__(self, path: str | Path = "dataiku_tutor/config/settings.yaml") -> None:
        self._path = Path(path)
        self._config = self._load_yaml(self._path)

    @staticmethod
    def _load_yaml(path: Path) -> dict[str, Any]:
        raw = path.read_text(encoding="utf-8")
        try:
            import yaml  # type: ignore

            return yaml.safe_load(raw) or {}
        except Exception:
            return Settings._parse_simple_yaml(raw)

    @staticmethod
    def _parse_simple_yaml(raw: str) -> dict[str, Any]:
        """Parse a minimal subset of YAML (nested maps) for dependency-free local usage."""
        root: dict[str, Any] = {}
        section: dict[str, Any] | None = None

        for line in raw.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if not line.startswith("  ") and stripped.endswith(":"):
                key = stripped[:-1].strip()
                section = {}
                root[key] = section
                continue

            if line.startswith("  ") and ":" in stripped and section is not None:
                key, value = stripped.split(":", 1)
                section[key.strip()] = Settings._coerce_scalar(value.strip())

        return root

    @staticmethod
    def _coerce_scalar(value: str) -> Any:
        if value in {"true", "True"}:
            return True
        if value in {"false", "False"}:
            return False
        if value in {"null", "None", ""}:
            return "" if value == "" else None
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    @property
    def raw(self) -> dict[str, Any]:
        return self._config

    def section(self, name: str) -> dict[str, Any]:
        section = self._config.get(name, {})
        return section if isinstance(section, dict) else {}
