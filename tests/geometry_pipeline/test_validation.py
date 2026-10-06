import json
from pathlib import Path

from geometry_pipeline.manifest import build_manifest
from geometry_pipeline.schema import ContentBlock
from geometry_pipeline.validation import validate_block

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTENT_ROOT = PROJECT_ROOT / "book_geometry" / "content"
GLOSSARY = PROJECT_ROOT / "src" / "geometry_pipeline" / "glossary_geometry.json"


def _load(relative_path: str) -> ContentBlock:
    path = CONTENT_ROOT / relative_path
    return ContentBlock.model_validate_json(path.read_text(encoding="utf-8"))


def test_pilot_definition_block_passes_deterministic_validation() -> None:
    block = _load("sections/01_angles/geo.p013.s13.definition-angle.json")
    report = validate_block(block, project_root=PROJECT_ROOT, glossary_path=GLOSSARY)

    assert report.passed, report.model_dump_json(indent=2)
    assert report.issues == []


def test_pilot_exercise_math_check_passes() -> None:
    block = _load("sections/01_angles/geo.p019.ex01.supplementary-angle.json")
    report = validate_block(block, project_root=PROJECT_ROOT, glossary_path=GLOSSARY)

    assert report.passed, report.model_dump_json(indent=2)


def test_manifest_covers_the_complete_angles_pilot() -> None:
    entries = build_manifest(CONTENT_ROOT, PROJECT_ROOT)

    block_ids = [entry.block_id for entry in entries]
    assert len(entries) == 33
    assert block_ids[0] == "geo.p009.s01.geometric-figures"
    assert block_ids[-1] == "geo.p020.ex07.two-intersecting-lines"
    assert "geo.p019.ex01.supplementary-angle" in block_ids
    assert all(len(entry.sha256) == 64 for entry in entries)


def test_complete_angles_pilot_has_no_validation_errors() -> None:
    failures = []
    for path in sorted((CONTENT_ROOT / "sections" / "01_angles").glob("*.json")):
        block = ContentBlock.model_validate_json(path.read_text(encoding="utf-8"))
        report = validate_block(block, project_root=PROJECT_ROOT, glossary_path=GLOSSARY)
        if not report.passed:
            failures.append(report.model_dump(mode="json"))

    assert failures == []


def test_schema_rejects_untracked_fields() -> None:
    path = CONTENT_ROOT / "sections/01_angles/geo.p013.s13.definition-angle.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["unexpected"] = True

    try:
        ContentBlock.model_validate(payload)
    except ValueError:
        return
    raise AssertionError("Schema accepted an undeclared field")
