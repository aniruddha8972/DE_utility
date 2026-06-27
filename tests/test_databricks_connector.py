from de_utility.connectors.databricks import DatabricksConnector


class FakeSpark:
    def __init__(self) -> None:
        self.executed_sql: list[str] = []
        self.tables: dict[str, list[dict[str, object]]] = {}

    def sql(self, query: str) -> "FakeResult":
        self.executed_sql.append(query)
        if query.startswith("CREATE SCHEMA"):
            return FakeResult()
        if query.startswith("CREATE TABLE"):
            return FakeResult()
        if query.startswith("SELECT"):
            return FakeResult(rows=self.tables.get("default.demo_table", []))
        raise AssertionError(f"Unexpected SQL: {query}")

    def createDataFrame(self, rows, schema=None):
        return FakeDataFrame(rows=rows, schema=schema)


class FakeDataFrame:
    def __init__(self, rows, schema=None) -> None:
        self.rows = rows
        self.schema = schema

    def write(self, mode: str = "append"):
        return FakeWriter(self.rows)


class FakeWriter:
    def __init__(self, rows) -> None:
        self.rows = rows

    def saveAsTable(self, table_name: str) -> None:
        self.rows = self.rows


class FakeResult:
    def __init__(self, rows=None) -> None:
        self.rows = rows or []

    def collect(self):
        return self.rows


def test_databricks_connector_creates_schema_and_writes_table() -> None:
    spark = FakeSpark()
    connector = DatabricksConnector(
        name="databricks-demo",
        table_name="demo_table",
        schema_name="default",
        catalog_name="main",
        spark=spark,
    )

    connector.write([{"id": 1, "value": 10}])

    assert "CREATE SCHEMA IF NOT EXISTS main.default" in spark.executed_sql
    assert "CREATE TABLE IF NOT EXISTS main.default.demo_table (id BIGINT, value BIGINT)" in spark.executed_sql
