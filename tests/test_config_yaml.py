from de_utility.config import PipelineConfig


def test_pipeline_config_loads_yaml() -> None:
    config = PipelineConfig.from_file("configs/pipeline.yaml")

    assert config.name == "databricks-demo"
    assert config.source == "databricks"
    assert config.destination == "databricks"
    assert config.batch_size == 500
    assert config.metadata["schema"] == "default"
