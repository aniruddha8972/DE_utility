from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class JobConfig:
    """Simple loader for YAML deployment configs used by Databricks jobs."""

    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data

    @classmethod
    def from_file(cls, path: str | Path) -> "JobConfig":
        with Path(path).open("r", encoding="utf-8") as handle:
            return cls(yaml.safe_load(handle) or {})
