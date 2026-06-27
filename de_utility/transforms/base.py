from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable


class Transform(ABC):
    """Base class for data transformations used in a pipeline."""

    def __init__(self, name: str | None = None) -> None:
        self.name = name or self.__class__.__name__

    @abstractmethod
    def transform(self, data: Any) -> Any:
        """Apply a transformation to the supplied payload."""


class MapTransform(Transform):
    """Apply a mapping function to each record in a list."""

    def __init__(self, func: Callable[[dict[str, Any]], dict[str, Any]], name: str | None = None) -> None:
        super().__init__(name)
        self._func = func

    def transform(self, data: Any) -> Any:
        if isinstance(data, list):
            return [self._func(item) for item in data]
        return self._func(data)


class FilterTransform(Transform):
    """Keep only rows that satisfy the predicate."""

    def __init__(self, predicate: Callable[[dict[str, Any]], bool], name: str | None = None) -> None:
        super().__init__(name)
        self._predicate = predicate

    def transform(self, data: Any) -> Any:
        if not isinstance(data, list):
            return data if self._predicate(data) else None
        return [item for item in data if self._predicate(item)]
