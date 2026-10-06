"""Validation gates for structured geometry content."""

from __future__ import annotations

import hashlib
import json
import re
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from .math_validation import run_math_check
from .schema import ContentBlock

FIGURE_REFERENCE_PATTERN = re.compile(r"\b(?:рис|черт)\.\s*~?\s*(\d+)\b", re.IGNORECASE)


def _contains_term(text: str, term: str) -> bool:
    """Match a glossary term as words, not as an arbitrary substring."""

    if not term:
        return False
    pattern = rf"(?<!\w){re.escape(term.casefold())}(?!\w)"
    return re.search(pattern, text.casefold()) is not None


class Severity(StrEnum):
    ERROR = "error"
    WARNING = "warning"


class ValidationIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    severity: Severity
    message: str
    field: str | None = None


class ValidationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    block_id: str
    issues: list[ValidationIssue] = Field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not any(issue.severity is Severity.ERROR for issue in self.issues)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_glossary(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def _validate_source(block: ContentBlock, project_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, source in enumerate(block.sources):
        source_image = project_root / source.source_image
        if not source_image.is_file():
            issues.append(
                ValidationIssue(
                    code="source.image_missing",
                    severity=Severity.ERROR,
                    field=f"sources.{index}.source_image",
                    message=f"Source image does not exist: {source_image}",
                )
            )
            continue

        if source.image_sha256 is None:
            issues.append(
                ValidationIssue(
                    code="source.hash_missing",
                    severity=Severity.WARNING,
                    field=f"sources.{index}.image_sha256",
                    message="Source image hash is not recorded",
                )
            )
        elif _sha256(source_image) != source.image_sha256:
            issues.append(
                ValidationIssue(
                    code="source.hash_mismatch",
                    severity=Severity.ERROR,
                    field=f"sources.{index}.image_sha256",
                    message="Source image hash does not match the manifest",
                )
            )
    return issues


def _validate_terminology(block: ContentBlock, glossary: dict) -> list[ValidationIssue]:
    if block.translation is None:
        return []

    issues: list[ValidationIssue] = []
    source_text = block.ocr.text_ru.casefold()
    translated_text = block.translation.text_uk.casefold()

    for term in glossary.get("terms", []):
        for forbidden in term.get("forbidden_uk_calques", []):
            if _contains_term(translated_text, forbidden):
                issues.append(
                    ValidationIssue(
                        code="terminology.forbidden_calque",
                        severity=Severity.ERROR,
                        field="translation.text_uk",
                        message=f"Forbidden term found: {forbidden}",
                    )
                )

        source_variants = [term.get("ru_archaic", ""), *term.get("ru_alternates", [])]
        source_term_present = any(
            _contains_term(source_text, variant) for variant in source_variants
        )
        targets = [
            term.get("uk_target", ""),
            *term.get("uk_alternates", []),
            term.get("uk_abbreviation", ""),
        ]
        accepted_targets = [target for target in targets if target]
        if (
            source_term_present
            and accepted_targets
            and not any(_contains_term(translated_text, target) for target in accepted_targets)
        ):
            issues.append(
                ValidationIssue(
                    code="terminology.expected_term_missing",
                    severity=Severity.WARNING,
                    field="translation.text_uk",
                    message=f"Expected glossary term is absent: {targets[0]}",
                )
            )
    return issues


def _validate_figure_references(block: ContentBlock) -> list[ValidationIssue]:
    text_parts = [block.ocr.text_ru]
    if block.translation:
        text_parts.append(block.translation.text_uk)
    text_parts.extend(item.text_uk for item in block.adaptations)
    referenced = {int(value) for value in FIGURE_REFERENCE_PATTERN.findall("\n".join(text_parts))}
    declared = {
        figure.source_number for figure in block.figures if figure.source_number is not None
    }
    missing = sorted(referenced - declared)
    return [
        ValidationIssue(
            code="figure.reference_missing",
            severity=Severity.ERROR,
            field="figures",
            message=f"Figure {number} is referenced but not declared",
        )
        for number in missing
    ]


def _validate_figure_assets(block: ContentBlock, project_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for index, figure in enumerate(block.figures):
        if not figure.vector_source:
            issues.append(
                ValidationIssue(
                    code="figure.vector_missing",
                    severity=Severity.WARNING,
                    field=f"figures.{index}.vector_source",
                    message=f"Figure {figure.id} has no vector source",
                )
            )
        elif not (project_root / figure.vector_source).is_file():
            issues.append(
                ValidationIssue(
                    code="figure.vector_not_found",
                    severity=Severity.ERROR,
                    field=f"figures.{index}.vector_source",
                    message=f"Vector source does not exist: {figure.vector_source}",
                )
            )
        if not figure.alt_uk:
            issues.append(
                ValidationIssue(
                    code="figure.alt_missing",
                    severity=Severity.WARNING,
                    field=f"figures.{index}.alt_uk",
                    message=f"Figure {figure.id} has no Ukrainian alternative text",
                )
            )
    return issues


def validate_block(
    block: ContentBlock,
    *,
    project_root: Path,
    glossary_path: Path,
) -> ValidationReport:
    """Apply deterministic validation gates to one content block."""

    issues = _validate_source(block, project_root)
    issues.extend(_validate_terminology(block, _load_glossary(glossary_path)))
    issues.extend(_validate_figure_references(block))
    issues.extend(_validate_figure_assets(block, project_root))

    for index, check in enumerate(block.math_checks):
        try:
            passed, message = run_math_check(check)
        except (TypeError, ValueError) as exc:
            passed, message = False, str(exc)
        if not passed:
            issues.append(
                ValidationIssue(
                    code="math.check_failed",
                    severity=Severity.ERROR,
                    field=f"math_checks.{index}",
                    message=message,
                )
            )

    return ValidationReport(block_id=block.id, issues=issues)
