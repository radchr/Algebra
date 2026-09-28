#!/usr/bin/env python3
"""Initialize a durable authoring package for one grade-7 STEM lesson."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

SUBJECTS = ("algebra", "geometry", "physics", "chemistry", "biology")
MODES = ("guided", "scenario", "quick")


def valid_slug(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value):
        raise argparse.ArgumentTypeError("slug must use lowercase letters, digits, and hyphens")
    return value


def write_new(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def legacy_notebook_manifest(project_root: Path) -> dict[str, str]:
    notebook_root = project_root / "notebooks"
    if not notebook_root.is_dir():
        return {}
    return {
        path.relative_to(project_root).as_posix(): file_sha256(path)
        for path in sorted(notebook_root.rglob("*"))
        if path.is_file() and path.suffix.lower() in {".py", ".ipynb"}
    }


def initialize(root: Path, slug: str, subject: str, mode: str, project_root: Path) -> tuple[Path, list[Path]]:
    lesson_dir = root / slug
    (lesson_dir / "audio" / "approved").mkdir(parents=True, exist_ok=True)
    (lesson_dir / "audio" / "takes").mkdir(parents=True, exist_ok=True)

    approval_bypassed = "true" if mode == "quick" else "false"
    brief = f"""---
lesson_id: TBD
slug: {slug}
subject: {subject}
grade: 7
status: draft
creation_mode: {mode}
approval_bypassed_by_user: {approval_bypassed}
---

# Робоча картка уроку

## Початкова ідея автора

## Головна думка уроку

## Питання, які потрібно розкрити

- [запропоновано] ...

## Типові помилки учня

## Візуальний дослід

### Що змінює учень

### Що залишається сталим

### Що спостерігає учень

### Що учень має зафіксувати

## Сюжет і персонажі

## Текст для екрана

## Ідеї для озвучення

## Потрібні артефакти
"""
    files = {
        "source_prompt.md": "",
        "lesson_brief.md": brief,
        "decisions.md": (
            "# Рішення автора і моделі\n\n| Дата | Рішення | Хто вирішив | Причина |\n|---|---|---|---|\n"
        ),
        "scenario.md": ("# Сценарій уроку\n\n_Очікує погодження робочої картки._\n"),
        "narration_ua.md": "# Озвучення\n\n_Очікує погодження сценарію._\n",
        "scenes.json": json.dumps(
            {
                "version": 1,
                "voice_profile": "single_ukrainian_voice",
                "scenes": [],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        "workflow.json": json.dumps(
            {
                "version": 1,
                "stage": "initialized",
                "brief_approval": None,
                "scenario_approval": None,
                "approval_bypassed_by_user": mode == "quick",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        "integrity.json": json.dumps(
            {
                "version": 1,
                "source_prompt_sha256": None,
                "locked_blocks_sha256": [],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        "legacy_notebooks.json": json.dumps(
            {
                "version": 1,
                "project_root": str(project_root.resolve()),
                "files": legacy_notebook_manifest(project_root.resolve()),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        "timeline.json": json.dumps({"version": 1, "scenes": []}, ensure_ascii=False, indent=2) + "\n",
        "audio_manifest.json": json.dumps(
            {
                "version": 1,
                "voice_profile": "single_ukrainian_voice",
                "clips": [],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    }
    created: list[Path] = []
    for name, content in files.items():
        target = lesson_dir / name
        if write_new(target, content):
            created.append(target)
    return lesson_dir, created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", type=valid_slug)
    parser.add_argument("--subject", required=True, choices=SUBJECTS)
    parser.add_argument("--mode", default="guided", choices=MODES)
    parser.add_argument("--root", type=Path, default=Path("authoring"))
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    lesson_dir, created = initialize(args.root, args.slug, args.subject, args.mode, args.project_root)
    print(f"Lesson directory: {lesson_dir.resolve()}")
    if created:
        print("Created:")
        for path in created:
            print(f"- {path}")
    else:
        print("No files overwritten; existing package reused.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
