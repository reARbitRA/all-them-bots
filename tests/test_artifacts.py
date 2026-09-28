from __future__ import annotations

import pytest

from src.autofreelance.artifacts import materialize_artifacts, validate_artifacts
from src.autofreelance.exceptions import ArtifactValidationError
from src.autofreelance.models import ArtifactFile


def valid_files() -> tuple[ArtifactFile, ...]:
    return (
        ArtifactFile("README.md", "# راهنمای اجرا\n\nبرای اجرا ابتدا وابستگی‌ها را نصب کنید.".encode()),
        ArtifactFile("src/main.py", b"def main():\n    return 0\n"),
    )


def test_materializes_valid_project(tmp_path):
    files = validate_artifacts(valid_files())
    output = materialize_artifacts(tmp_path / "project", files)
    assert (output / "README.md").read_text(encoding="utf-8").startswith("# راهنمای")
    assert (output / "src/main.py").exists()


@pytest.mark.parametrize("path", ["../secret.txt", "/etc/passwd", ".git/config", "src/../../x.py"])
def test_rejects_unsafe_paths(path: str):
    files = (
        ArtifactFile("README.md", "# اجرا\nراهنما".encode()),
        ArtifactFile(path, b"no"),
    )
    with pytest.raises(ArtifactValidationError):
        validate_artifacts(files)


def test_rejects_non_persian_readme():
    with pytest.raises(ArtifactValidationError, match="Persian"):
        validate_artifacts((ArtifactFile("README.md", b"# Run\nInstall and execute."),))
