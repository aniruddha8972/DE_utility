from pathlib import Path


def test_ci_workflow_creates_maven_style_zip() -> None:
    workflow_path = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"
    workflow_content = workflow_path.read_text()

    assert "Create Maven-style zip" in workflow_content
    assert "git archive" in workflow_content
    assert "target/" in workflow_content
    assert "upload-artifact" in workflow_content


def test_release_workflow_creates_release_zip() -> None:
    workflow_path = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "release.yml"
    workflow_content = workflow_path.read_text()

    assert "Create Maven-style zip" in workflow_content
    assert "git archive" in workflow_content
    assert "github.event.inputs.release_tag || github.ref_name" in workflow_content
    assert "GITHUB_WORKSPACE" in workflow_content
    assert "release-tags.txt" in workflow_content
    assert "upload-artifact" in workflow_content
