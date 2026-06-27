from pathlib import Path


def test_release_workflow_creates_release_zip() -> None:
    workflow_path = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "release.yml"
    workflow_content = workflow_path.read_text()

    assert "Create release zip" in workflow_content
    assert "git archive" in workflow_content
    assert "GITHUB_REF_NAME" in workflow_content
    assert "upload-artifact" in workflow_content
