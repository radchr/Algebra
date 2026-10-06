"""Content-addressed manifest helpers for resumable agent work."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from .schema import ContentBlock, ReviewStatus


class ManifestEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    block_id: str
    file: str
    sha256: str
    stage: str


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def block_stage(block: ContentBlock) -> str:
    if block.translation is None:
        return "ocr"
    if block.qa.human_review is ReviewStatus.APPROVED:
        return "approved"
    if block.adaptations:
        return "adapted"
    return "translated"


def build_manifest(content_root: Path, project_root: Path) -> list[ManifestEntry]:
    entries: list[ManifestEntry] = []
    for path in sorted(content_root.rglob("*.json")):
        block = ContentBlock.model_validate_json(path.read_text(encoding="utf-8"))
        entries.append(
            ManifestEntry(
                block_id=block.id,
                file=path.relative_to(project_root).as_posix(),
                sha256=file_sha256(path),
                stage=block_stage(block),
            )
        )
    return entries


def write_manifest(entries: list[ManifestEntry], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(output_path.suffix + ".tmp")
    payload = "\n".join(entry.model_dump_json() for entry in entries)
    temp_path.write_text(payload + ("\n" if payload else ""), encoding="utf-8")
    os.replace(temp_path, output_path)
