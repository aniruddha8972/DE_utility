from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Connector(ABC, Generic[T]):
    """Abstract interface for pipeline input and output connectors."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def read(self) -> T:
        """Read payload from the underlying source."""

    @abstractmethod
    def write(self, payload: T) -> None:
        """Write payload to the underlying destination."""

    def close(self) -> None:
        """Release any resources held by the connector."""


class InMemoryConnector(Connector[list[dict[str, Any]]]):
    """A simple in-memory connector for local development and testing."""

    def __init__(self, name: str = "in-memory", initial_data: list[dict[str, Any]] | None = None) -> None:
        super().__init__(name)
        self._data = initial_data or []

    def read(self) -> list[dict[str, Any]]:
        return list(self._data)

    def write(self, payload: list[dict[str, Any]]) -> None:
        self._data = list(payload)
