from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_pyproject_metadata_identifies_fable_omega_runtime() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]

    assert project["name"] == "fable-omega"
    assert "FABLE OMEGA" in project["description"]
    assert "Telegram scenario runtime" in project["description"]
    assert project["authors"] == [{"name": "FABLE OMEGA maintainers"}]
    assert "autofreelance" not in project["name"].lower()
    assert "autofreelance" not in project["description"].lower()


def test_pyproject_entry_point_and_package_paths_target_runtime() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    scripts = pyproject["project"]["scripts"]
    assert scripts == {"fable-omega": "src.cli:main"}

    wheel_packages = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]["packages"]
    assert wheel_packages == ["src"]
