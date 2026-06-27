# DE_utility

A lightweight Python framework for building data engineering utility pipelines.

## What’s included
- Config-driven pipeline setup with PipelineConfig
- Generic connectors for reading and writing data
- Transform steps such as mapping and filtering
- A small test suite demonstrating a working pipeline

## Project structure
- de_utility/config.py: configuration model
- de_utility/connectors/: connector abstractions and in-memory implementation
- de_utility/pipelines/: pipeline execution logic
- de_utility/transforms/: reusable transformation steps
- tests/: example tests and future regression coverage

## Quick example
```python
from de_utility.config import PipelineConfig
from de_utility.connectors.base import InMemoryConnector
from de_utility.pipelines.base import Pipeline
from de_utility.transforms.base import FilterTransform, MapTransform

config = PipelineConfig(name="demo")
source = InMemoryConnector(initial_data=[{"id": 1, "value": 10}, {"id": 2, "value": 20}])
destination = InMemoryConnector()

pipeline = Pipeline(
    config=config,
    source=source,
    destination=destination,
    transforms=[
        FilterTransform(lambda row: row["value"] >= 20),
        MapTransform(lambda row: {**row, "value": row["value"] * 2}),
    ],
)

result = pipeline.run()
print(result)
```

## Databricks Free Tier notes
This framework can target Databricks Free Tier environments by using the Databricks connector. It creates the target schema in the default workspace/catalog context, using the pattern:

```sql
CREATE SCHEMA IF NOT EXISTS main.default
CREATE TABLE IF NOT EXISTS main.default.demo_table
```

Example:
```python
from de_utility.connectors.databricks import DatabricksConnector

connector = DatabricksConnector(
    name="databricks-demo",
    table_name="demo_table",
    schema_name="default",
    catalog_name="main",
    spark=spark,
)
connector.write([{"id": 1, "value": 10}])
```

## YAML configuration and job deployment
The repository now includes sample YAML files for pipeline config and Databricks job deployment:
- configs/pipeline.yaml: pipeline settings
- configs/job_deployment.yaml: Databricks job definition

Example usage:
```python
from de_utility.config import PipelineConfig
from de_utility.job_config import JobConfig

pipeline_config = PipelineConfig.from_file("configs/pipeline.yaml")
job_config = JobConfig.from_file("configs/job_deployment.yaml")
print(pipeline_config.name)
print(job_config.data["name"])
```

## CI and release workflows
GitHub Actions workflows are included for automation:
- .github/workflows/ci.yml: runs tests on pushes and pull requests
- .github/workflows/release.yml: runs tests, builds the package, and publishes to PyPI when a version tag like v0.1.0 is pushed

## Verify locally
```bash
pytest -q
```