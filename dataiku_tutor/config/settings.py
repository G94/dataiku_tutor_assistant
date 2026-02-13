"""Configuration access layer backed by YAML settings."""

from pathlib import Path
from typing import Any

import yaml


class Settings:
    """Loads and exposes typed configuration sections."""

    def __init__(self, path: str | Path = "dataiku_tutor/config/settings.yaml") -> None:
        self._path = Path(path)
        self._config = self._load_yaml(self._path)

    @staticmethod
    def _load_yaml(path: Path) -> dict[str, Any]:
        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    @property
    def raw(self) -> dict[str, Any]:
        return self._config

    def section(self, name: str) -> dict[str, Any]:
        return self._config.get(name, {})
