from __future__ import annotations

import tomllib
from pathlib import Path

from packaging.requirements import Requirement

ROOT = Path(__file__).resolve().parent.parent


def _requirements_from_pyproject() -> set[str]:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pyproject["project"]
    values = list(project.get("dependencies", []))
    for group in project.get("optional-dependencies", {}).values():
        values.extend(group)
    return {Requirement(item).name.lower().replace("_", "-") for item in values}


def _requirements_txt() -> set[str]:
    names: set[str] = set()
    for line in (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        names.add(Requirement(line).name.lower().replace("_", "-"))
    return names


def test_requirements_txt_entries_are_declared_in_pyproject() -> None:
    assert _requirements_txt() <= _requirements_from_pyproject()
