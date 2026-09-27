"""Validation and safe materialization of untrusted generated project artifacts."""

from __future__ import annotations

import base64
import binascii
from pathlib import Path, PurePosixPath

from .exceptions import ArtifactValidationError
from .models import ArtifactFile
from .text import has_persian_text

MAX_FILE_COUNT = 2_000
MAX_FILE_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 50 * 1024 * 1024


def validate_artifacts(files: tuple[ArtifactFile, ...]) -> tuple[ArtifactFile, ...]:
    if not files:
        raise ArtifactValidationError("Executor returned no files")
    if len(files) > MAX_FILE_COUNT:
        raise ArtifactValidationError(f"Artifact count exceeds {MAX_FILE_COUNT}")
    total = 0
    normalized: list[ArtifactFile] = []
    paths: set[str] = set()
    for item in files:
        safe_path = validate_relative_path(item.path)
        if safe_path in paths:
            raise ArtifactValidationError(f"Duplicate artifact path: {safe_path}")
        paths.add(safe_path)
        if len(item.content) > MAX_FILE_BYTES:
            raise ArtifactValidationError(f"Artifact exceeds {MAX_FILE_BYTES} bytes: {safe_path}")
        total += len(item.content)
        if total > MAX_TOTAL_BYTES:
            raise ArtifactValidationError(f"Artifacts exceed {MAX_TOTAL_BYTES} bytes in total")
        normalized.append(ArtifactFile(path=safe_path, content=item.content))
    _validate_persian_readme(normalized)
    return tuple(normalized)


def validate_relative_path(value: str) -> str:
    if not value or len(value) > 240 or "\x00" in value:
        raise ArtifactValidationError("Invalid artifact path")
    candidate = PurePosixPath(value.replace("\\", "/"))
    if candidate.is_absolute() or ".." in candidate.parts or candidate.name in {"", ".", ".."}:
        raise ArtifactValidationError(f"Unsafe artifact path: {value}")
    if candidate.parts[0].lower() in {".git", ".github"}:
        raise ArtifactValidationError(f"Artifact path is not allowed: {value}")
    return candidate.as_posix()


def materialize_artifacts(root: Path, files: tuple[ArtifactFile, ...]) -> Path:
    """Write validated artifacts beneath ``root`` without following arbitrary paths."""
    checked = validate_artifacts(files)
    root.mkdir(parents=True, exist_ok=True)
    root_resolved = root.resolve()
    for item in checked:
        destination = (root / item.path).resolve()
        if root_resolved not in destination.parents and destination != root_resolved:
            raise ArtifactValidationError(f"Artifact escaped root: {item.path}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(item.content)
    return root_resolved


def decode_base64(value: str, path: str) -> bytes:
    try:
        return base64.b64decode(value, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise ArtifactValidationError(f"Invalid base64 content for {path}") from exc


def _validate_persian_readme(files: list[ArtifactFile]) -> None:
    readmes = [item for item in files if item.path.casefold() == "readme.md"]
    if len(readmes) != 1:
        raise ArtifactValidationError("Exactly one root README.md is required")
    try:
        readme = readmes[0].content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ArtifactValidationError("README.md must be valid UTF-8") from exc
    instructions = ("اجرا", "نصب", "راه‌اندازی", "راه اندازی")
    if not has_persian_text(readme) or not any(term in readme for term in instructions):
        raise ArtifactValidationError("README.md must include Persian execution instructions")
