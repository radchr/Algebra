#!/usr/bin/env python3
"""Validate deterministic invariants of a STEM lesson authoring package."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

REQUIRED_FILES = (
    "source_prompt.md",
    "lesson_brief.md",
    "decisions.md",
    "scenario.md",
    "narration_ua.md",
    "scenes.json",
    "workflow.json",
    "integrity.json",
    "legacy_notebooks.json",
    "timeline.json",
    "audio_manifest.json",
)
SUBJECTS = {"algebra", "geometry", "physics", "chemistry", "biology"}
TEXT_EXTENSIONS = {
    ".css",
    ".htm",
    ".html",
    ".ipynb",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
LOCKED_BLOCK = re.compile(r"\[ЗБЕРЕГТИ ДОСЛІВНО\](.*?)\[/ЗБЕРЕГТИ ДОСЛІВНО\]", re.DOTALL)
FORBIDDEN_NARRATION_PATTERNS = {
    "raw digit": re.compile(r"\d|[⁰¹²³⁴⁵⁶⁷⁸⁹]"),
    "LaTeX or code markup": re.compile(r"\$|\\[A-Za-z]+|\\\(|\\\)|\\\[|\\\]|`"),
    "formula operator": re.compile(r"[=+*/<>^%×÷≤≥≈]|_\{"),
    "raw Latin text": re.compile(r"[A-Za-z]"),
    "abbreviated unit": re.compile(
        r"(?<!\w)(?:кг|г|м|см|мм|км|л|мл|с|мс|па|кпа|н|дж|вт|гц|°c)(?!\w)",
        re.IGNORECASE,
    ),
    "stage direction": re.compile(r"\[[^\]]+\]|<[^>]+>|\b(?:pause|break)\b", re.IGNORECASE),
    "URL or file path": re.compile(r"https?://|www\.|[A-Za-z]:\\|(?:^|\s)[./\\][^\s]+", re.IGNORECASE),
}
FORBIDDEN_LEARNER_TERMS = re.compile(
    r"\b(?:POEM|P-O-E-M|BKT|Bayesian Knowledge Tracing|misconception[_ -]?id|"
    r"author[_ -]?note|mastery[_ -]?(?:score|probability)|internal[_ -]?model)\b|"
    r"баєс(?:ів|ов)|ідентифікатор\s+помилки|нотатк\w*\s+автора|"
    r"ймовірн\w*\s+засвоєння",
    re.IGNORECASE,
)
EXTERNAL_HTTP = re.compile(
    r"https?://(?!127\.0\.0\.1(?::\d+)?(?:/|$)|localhost(?::\d+)?(?:/|$))",
    re.IGNORECASE,
)
PROTOCOL_RELATIVE_CDN = re.compile(r"//[a-z0-9.-]+\.[a-z]{2,}(?:/|\b)", re.IGNORECASE)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path, errors: list[str]) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid {path.name}: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append(f"{path.name} must contain a JSON object")
        return {}
    return data


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


def parse_narration(text: str) -> tuple[dict[str, str], list[str]]:
    result: dict[str, str] = {}
    errors: list[str] = []
    current: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("## "):
            current = stripped[3:].strip()
            if current in result:
                errors.append(f"duplicate narration heading: {current}")
            result.setdefault(current, "")
        elif stripped.lower().startswith("text:"):
            if current is None:
                errors.append("narration text appears before a scene heading")
            else:
                result[current] = stripped.split(":", 1)[1].strip()
    return result, errors


def narration_errors(payload: str, context: str) -> list[str]:
    return [
        f"{context} contains {label}"
        for label, pattern in FORBIDDEN_NARRATION_PATTERNS.items()
        if pattern.search(payload)
    ]


def collect_learner_files(explicit: list[Path], roots: list[Path], errors: list[str]) -> list[Path]:
    files: set[Path] = set()
    for path in explicit:
        if path.is_file():
            files.add(path.resolve())
        else:
            errors.append(f"learner file not found: {path}")
    for root in roots:
        if not root.is_dir():
            errors.append(f"learner root not found: {root}")
            continue
        files.update(
            path.resolve() for path in root.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS
        )
    return sorted(files)


def validate_lesson(
    lesson_dir: Path,
    learner_files: list[Path],
    learner_roots: list[Path],
    require_audio: bool,
    final: bool,
    require_offline: bool,
    project_root: Path,
) -> list[str]:
    errors: list[str] = []
    final = final or require_audio
    for name in REQUIRED_FILES:
        if not (lesson_dir / name).is_file():
            errors.append(f"missing required file: {name}")

    brief_path = lesson_dir / "lesson_brief.md"
    source_path = lesson_dir / "source_prompt.md"
    meta: dict[str, str] = {}
    brief = ""
    source = ""
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
    if source_path.is_file():
        source = source_path.read_text(encoding="utf-8")
        if final and not source:
            errors.append("source_prompt.md is empty")
        if source and source not in brief:
            errors.append("exact source prompt is absent from lesson_brief.md")

    integrity_path = lesson_dir / "integrity.json"
    if integrity_path.is_file():
        integrity = load_json(integrity_path, errors)
        expected_source = integrity.get("source_prompt_sha256")
        if final and not expected_source:
            errors.append("source prompt integrity has not been sealed")
        elif expected_source and expected_source != sha256_text(source):
            errors.append("source_prompt.md differs from its integrity seal")
        expected_locked = integrity.get("locked_blocks_sha256", [])
        actual_locked = [sha256_text(block) for block in LOCKED_BLOCK.findall(brief)]
        if expected_source and expected_locked != actual_locked:
            errors.append("locked text differs from its integrity seal")

    workflow_path = lesson_dir / "workflow.json"
    if workflow_path.is_file() and final:
        workflow = load_json(workflow_path, errors)
        quick = meta.get("creation_mode") == "quick"
        bypassed = workflow.get("approval_bypassed_by_user") is True
        if quick and not bypassed:
            errors.append("quick mode must record the user-requested bypass")
        elif not quick and not workflow.get("brief_approval"):
            errors.append("brief approval is not recorded")
        elif not quick and not workflow.get("scenario_approval"):
            errors.append("scenario approval is not recorded")

    narration_map: dict[str, str] = {}
    narration_path = lesson_dir / "narration_ua.md"
    if narration_path.is_file():
        narration_map, parse_errors = parse_narration(narration_path.read_text(encoding="utf-8"))
        errors.extend(parse_errors)
        for scene_id, payload in narration_map.items():
            if final and not payload:
                errors.append(f"narration is empty for {scene_id}")
            errors.extend(narration_errors(payload, f"narration {scene_id}"))

    scenes: list[dict] = []
    scene_ids: list[str] = []
    scenes_path = lesson_dir / "scenes.json"
    if scenes_path.is_file():
        scenes_data = load_json(scenes_path, errors)
        if scenes_data.get("voice_profile") != "single_ukrainian_voice":
            errors.append("scenes.json must use the single Ukrainian voice profile")
        raw_scenes = scenes_data.get("scenes")
        if not isinstance(raw_scenes, list):
            errors.append("scenes.json must contain a scenes list")
        else:
            scenes = [scene for scene in raw_scenes if isinstance(scene, dict)]
            if len(scenes) != len(raw_scenes):
                errors.append("every scene must be a JSON object")
            if final and not scenes:
                errors.append("final package must contain at least one scene")
            for index, scene in enumerate(scenes):
                scene_id = str(scene.get("id", "")).strip()
                if not scene_id:
                    errors.append(f"scene at index {index} has no id")
                    continue
                if scene_id in scene_ids:
                    errors.append(f"duplicate scene id: {scene_id}")
                scene_ids.append(scene_id)
                payload = str(scene.get("narration", "")).strip()
                if final and not payload:
                    errors.append(f"scene {scene_id} has empty narration")
                errors.extend(narration_errors(payload, f"scene {scene_id} narration"))
                if narration_map.get(scene_id) != payload:
                    errors.append(f"narration_ua.md and scenes.json differ for {scene_id}")
            for scene_id in sorted(set(narration_map) - set(scene_ids)):
                errors.append(f"narration has no matching scene: {scene_id}")

    if require_audio:
        takes_root = lesson_dir / "audio" / "takes"
        manifest = load_json(lesson_dir / "audio_manifest.json", errors)
        timeline = load_json(lesson_dir / "timeline.json", errors)
        if manifest.get("voice_profile") != "single_ukrainian_voice":
            errors.append("audio manifest must use one Ukrainian voice")
        clips = manifest.get("clips", [])
        timeline_scenes = timeline.get("scenes", [])
        clip_by_id = {str(item.get("id")): item for item in clips if isinstance(item, dict) and item.get("id")}
        timeline_by_id = {
            str(item.get("id")): item for item in timeline_scenes if isinstance(item, dict) and item.get("id")
        }
        if len(clip_by_id) != len(clips):
            errors.append("audio manifest contains duplicate or invalid clip ids")
        if len(timeline_by_id) != len(timeline_scenes):
            errors.append("timeline contains duplicate or invalid scene ids")
        for scene in scenes:
            scene_id = str(scene.get("id", ""))
            duration = scene.get("duration_seconds")
            if not isinstance(duration, (int, float)) or duration <= 0:
                errors.append(f"scene {scene_id} has no positive duration")
            audio_rel = str(scene.get("audio", ""))
            audio_path = lesson_dir / audio_rel
            if (
                not audio_rel.startswith("audio/approved/")
                or audio_path.suffix.lower() not in {".wav", ".mp3", ".m4a"}
                or not audio_path.is_file()
            ):
                errors.append(f"missing approved audio for {scene_id}")
            elif audio_path.stat().st_size == 0:
                errors.append(f"approved audio is empty for {scene_id}")
            take_dir = takes_root / scene_id
            candidates = (
                [
                    path
                    for path in take_dir.glob("*")
                    if path.is_file() and path.suffix.lower() in {".wav", ".mp3", ".m4a"} and path.stat().st_size > 0
                ]
                if take_dir.is_dir()
                else []
            )
            if not candidates:
                errors.append(f"no preserved candidate take for {scene_id}")
            clip = clip_by_id.get(scene_id)
            if not clip:
                errors.append(f"audio manifest has no clip for {scene_id}")
            else:
                if clip.get("approved") != audio_rel:
                    errors.append(f"audio manifest path mismatch for {scene_id}")
                if clip.get("duration_seconds") != duration:
                    errors.append(f"audio manifest duration mismatch for {scene_id}")
                if clip.get("narration_sha256") != sha256_text(str(scene.get("narration", ""))):
                    errors.append(f"audio narration hash mismatch for {scene_id}")
                for previous in clip.get("previous_approved", []):
                    if not (lesson_dir / str(previous)).is_file():
                        errors.append(f"missing preserved previous audio for {scene_id}: {previous}")
            timeline_item = timeline_by_id.get(scene_id)
            if not timeline_item or timeline_item.get("duration_seconds") != duration:
                errors.append(f"timeline duration mismatch for {scene_id}")
        if set(clip_by_id) != set(scene_ids):
            errors.append("audio manifest scene ids differ from scenes.json")
        if set(timeline_by_id) != set(scene_ids):
            errors.append("timeline scene ids differ from scenes.json")

    files = collect_learner_files(learner_files, learner_roots, errors)
    if final and not files:
        errors.append("final validation requires a learner file or learner root")
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if FORBIDDEN_LEARNER_TERMS.search(text):
            errors.append(f"learner file exposes internal authoring data: {path}")
        if require_offline and (EXTERNAL_HTTP.search(text) or PROTOCOL_RELATIVE_CDN.search(text)):
            errors.append(f"learner file contains an external runtime URL: {path}")

    legacy_path = lesson_dir / "legacy_notebooks.json"
    if legacy_path.is_file() and final:
        legacy = load_json(legacy_path, errors)
        baseline = legacy.get("files")
        if not isinstance(baseline, dict):
            errors.append("legacy notebook baseline is invalid")
        else:
            notebook_root = project_root / "notebooks"
            current = (
                {
                    path.relative_to(project_root).as_posix(): file_sha256(path)
                    for path in sorted(notebook_root.rglob("*"))
                    if path.is_file() and path.suffix.lower() in {".py", ".ipynb"}
                }
                if notebook_root.is_dir()
                else {}
            )
            baseline_changed = any(current.get(path) != digest for path, digest in baseline.items())
            if baseline_changed:
                errors.append("legacy notebooks changed after lesson initialization")

    if final:
        scenario_path = lesson_dir / "scenario.md"
        if scenario_path.is_file():
            scenario = scenario_path.read_text(encoding="utf-8")
            if "Очікує погодження" in scenario or "## Сцена" not in scenario:
                errors.append("scenario.md is still a placeholder or has no scenes")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson_dir", type=Path)
    parser.add_argument("--learner-file", action="append", type=Path, default=[])
    parser.add_argument("--learner-root", action="append", type=Path, default=[])
    parser.add_argument("--require-audio", action="store_true")
    parser.add_argument("--final", action="store_true")
    parser.add_argument(
        "--require-offline",
        action="store_true",
        help="reject external HTTP and CDN runtime dependencies",
    )
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = validate_lesson(
        args.lesson_dir,
        args.learner_file,
        args.learner_root,
        args.require_audio,
        args.final,
        args.require_offline,
        args.project_root.resolve(),
    )
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
