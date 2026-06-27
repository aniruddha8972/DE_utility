from __future__ import annotations

from typing import Any

from .base import Connector


class DatabricksConnector(Connector[list[dict[str, Any]]]):
    """A connector tailored for Databricks Free Tier usage.

    It creates the target schema in the default workspace/catalog context and writes
    to a table inside that schema.
    """

    def __init__(
        self,
        name: str,
        table_name: str,
        schema_name: str = "default",
        catalog_name: str = "main",
        spark: Any | None = None,
    ) -> None:
        super().__init__(name)
        self.table_name = table_name
        self.schema_name = schema_name
        self.catalog_name = catalog_name
        self.spark = spark

    def _ensure_schema(self) -> None:
        if self.spark is None:
            return
        self.spark.sql(f"CREATE SCHEMA IF NOT EXISTS {self.catalog_name}.{self.schema_name}")

    def _ensure_table(self) -> None:
        if self.spark is None:
            return
        self.spark.sql(
            f"CREATE TABLE IF NOT EXISTS {self.catalog_name}.{self.schema_name}.{self.table_name} "
            f"(id BIGINT, value BIGINT)"
        )

    def read(self) -> list[dict[str, Any]]:
        if self.spark is None:
            return []
        rows = self.spark.sql(
            f"SELECT * FROM {self.catalog_name}.{self.schema_name}.{self.table_name}"
        ).collect()
        return [dict(row) for row in rows]

    def write(self, payload: list[dict[str, Any]]) -> None:
        if self.spark is None:
            return
        self._ensure_schema()
        self._ensure_table()
        self.spark.createDataFrame(payload).write(mode="overwrite").saveAsTable(
            f"{self.catalog_name}.{self.schema_name}.{self.table_name}"
        )
