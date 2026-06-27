from __future__ import annotations

from typing import Any, Sequence

from ..config import PipelineConfig
from ..connectors.base import Connector
from ..transforms.base import Transform


class Pipeline:
    """A simple sequential pipeline for data transformation workflows."""

    def __init__(self, config: PipelineConfig, source: Connector[Any], destination: Connector[Any], transforms: Sequence[Transform] | None = None) -> None:
        self.config = config
        self.source = source
        self.destination = destination
        self.transforms = list(transforms or [])

    def run(self) -> Any:
        data = self.source.read()
        for transform in self.transforms:
            data = transform.transform(data)
        self.destination.write(data)
        return data
