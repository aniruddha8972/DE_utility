from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class PipelineConfig:
    """Configuration values used to run a data engineering pipeline."""

    name: str
    source: str = "memory"
    destination: str = "memory"
    batch_size: int = 1000
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_file(cls, path: str | Path) -> "PipelineConfig":
        file_path = Path(path)
        if file_path.suffix.lower() == ".yaml":
            raw = yaml.safe_load(file_path.read_text(encoding="utf-8")) or {}
        else:
            raw = json.loads(file_path.read_text(encoding="utf-8"))
        return cls(**raw)
