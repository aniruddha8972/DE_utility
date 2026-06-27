from de_utility.config import PipelineConfig
from de_utility.connectors.base import InMemoryConnector
from de_utility.pipelines.base import Pipeline
from de_utility.transforms.base import FilterTransform, MapTransform


def test_pipeline_runs_transforms() -> None:
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

    assert result == [{"id": 2, "value": 40}]
    assert destination.read() == [{"id": 2, "value": 40}]
