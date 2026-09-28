#!/usr/bin/env python3
"""Validate deterministic invariants of a STEM lesson authoring package."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_FILES = (
    "lesson_brief.md",
    "decisions.md",
    "scenario.md",
    "narration_ua.md",
    "scenes.json",
)
SUBJECTS = {"algebra", "geometry", "physics", "chemistry", "biology"}
FORBIDDEN_NARRATION_PATTERNS = {
    "raw digit": re.compile(r"\d"),
    "LaTeX delimiter": re.compile(r"\$|\\\(|\\\)|\\\[|\\\]"),
    "LaTeX command": re.compile(r"\\(?:frac|dfrac|text|rho|cdot|sqrt|begin|end)\b"),
    "formula operator": re.compile(r"(?:\^|_\{|==|!=|<=|>=)"),
    "URL": re.compile(r"https?://", re.IGNORECASE),
}
FORBIDDEN_LEARNER_TERMS = re.compile(
    r"\b(?:POEM|P-O-E-M|BKT|Bayesian Knowledge Tracing)\b|баєс(?:ів|ов)",
    re.IGNORECASE,
)
EXTERNAL_URL = re.compile(
    r"https?://(?!127\.0\.0\.1(?::\d+)?(?:/|$)|localhost(?::\d+)?(?:/|$))",
    re.IGNORECASE,
)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    try:
        raw = text.split("---\n", 2)[1]
    except IndexError:
        return {}
    result: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip("\"'")
    return result


def narration_payloads(text: str) -> list[str]:
    """Return only text intended for TTS, not Markdown headings or metadata."""
    explicit = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("text:"):
            explicit.append(stripped.split(":", 1)[1].strip())
    if explicit:
        return [payload for payload in explicit if payload]

    ignored_prefixes = ("#", "_", "speaker:", "emotion:", "audio:")
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().lower().startswith(ignored_prefixes)
    ]


def validate_lesson(lesson_dir: Path, learner_files: list[Path], require_audio: bool) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_FILES:
        if not (lesson_dir / name).is_file():
            errors.append(f"missing required file: {name}")

    brief_path = lesson_dir / "lesson_brief.md"
    if brief_path.is_file():
        brief = brief_path.read_text(encoding="utf-8")
        meta = parse_frontmatter(brief)
        if meta.get("grade") != "7":
            errors.append("lesson_brief.md must declare grade: 7")
        if meta.get("subject") not in SUBJECTS:
            errors.append("lesson_brief.md has an unsupported subject")
        if meta.get("creation_mode") not in {"guided", "scenario", "quick"}:
            errors.append("lesson_brief.md has an unsupported creation_mode")
        if brief.count("[ЗБЕРЕГТИ ДОСЛІВНО]") != brief.count("[/ЗБЕРЕГТИ ДОСЛІВНО]"):
            errors.append("unbalanced locked-text markers in lesson_brief.md")

    narration_path = lesson_dir / "narration_ua.md"
    if narration_path.is_file():
        narration = narration_path.read_text(encoding="utf-8")
        for payload in narration_payloads(narration):
            for label, pattern in FORBIDDEN_NARRATION_PATTERNS.items():
                if pattern.search(payload):
                    errors.append(f"narration contains {label}")

    scenes_path = lesson_dir / "scenes.json"
    scene_ids: list[str] = []
    if scenes_path.is_file():
        try:
            data = json.loads(scenes_path.read_text(encoding="utf-8"))
            scenes = data.get("scenes")
            if not isinstance(scenes, list):
                errors.append("scenes.json must contain a scenes list")
            else:
                for index, scene in enumerate(scenes):
                    if not isinstance(scene, dict) or not scene.get("id"):
                        errors.append(f"scene at index {index} has no id")
                    else:
                        scene_ids.append(str(scene["id"]))
                    narration = str(scene.get("narration", "")) if isinstance(scene, dict) else ""
                    for label, pattern in FORBIDDEN_NARRATION_PATTERNS.items():
                        if pattern.search(narration):
                            errors.append(f"scene {index} narration contains {label}")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid scenes.json: {exc}")

    if require_audio:
        approved = lesson_dir / "audio" / "approved"
        for scene_id in scene_ids:
            if not any((approved / f"{scene_id}{suffix}").is_file() for suffix in (".wav", ".mp3", ".m4a")):
                errors.append(f"missing approved audio for {scene_id}")

    for path in learner_files:
        if not path.is_file():
            errors.append(f"learner file not found: {path}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if FORBIDDEN_LEARNER_TERMS.search(text):
            errors.append(f"learner file exposes internal pedagogy: {path}")
        if EXTERNAL_URL.search(text):
            errors.append(f"learner file contains an external runtime URL: {path}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson_dir", type=Path)
    parser.add_argument("--learner-file", action="append", type=Path, default=[])
    parser.add_argument("--require-audio", action="store_true")
    args = parser.parse_args()

    errors = validate_lesson(args.lesson_dir, args.learner_file, args.require_audio)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    from validate_lesson_v2 import main as validated_main

    raise SystemExit(validated_main())
