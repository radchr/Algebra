"""Typed contracts for OCR, translation, adaptation, and mathematical QA."""

from __future__ import annotations

import re
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

BLOCK_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]+$")


class StrictModel(BaseModel):
    """Base model that rejects undeclared fields."""

    model_config = ConfigDict(extra="forbid")


class ReviewStatus(StrEnum):
    PENDING = "pending"
    GENERATED = "generated"
    NEEDS_REVIEW = "needs_review"
    APPROVED = "approved"
    REJECTED = "rejected"


class BlockKind(StrEnum):
    PARAGRAPH = "paragraph"
    DEFINITION = "definition"
    THEOREM = "theorem"
    PROOF = "proof"
    EXERCISE = "exercise"
    SOLUTION = "solution"
    FIGURE = "figure"


class AdaptationKind(StrEnum):
    TERMINOLOGY = "terminology_adaptation"
    EDITORIAL_EXPLANATION = "editorial_explanation"
    MISCONCEPTION = "misconception"
    PROOF_GUIDE = "proof_guide"
    HISTORICAL_NOTE = "historical_note"
    WORKED_SOLUTION = "worked_solution"
    INTERACTIVE_LINK = "interactive_link"


class BoundingBox(StrictModel):
    left: int = Field(ge=0)
    top: int = Field(ge=0)
    right: int = Field(gt=0)
    bottom: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_extent(self) -> BoundingBox:
        if self.right <= self.left or self.bottom <= self.top:
            raise ValueError("Bounding box must have positive width and height")
        return self


class SourceReference(StrictModel):
    pdf_path: str
    pdf_page: int = Field(ge=1)
    printed_page: int | None = Field(default=None, ge=1)
    section: str
    source_image: str
    image_sha256: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    bbox: BoundingBox | None = None


class OCRRecord(StrictModel):
    text_ru: str = Field(min_length=1)
    engine: str
    model: str | None = None
    prompt_version: str
    run_id: str
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    status: ReviewStatus = ReviewStatus.NEEDS_REVIEW


class TranslationRecord(StrictModel):
    text_uk: str = Field(min_length=1)
    model: str | None = None
    prompt_version: str
    glossary_version: str
    omissions: list[str] = Field(default_factory=list)
    status: ReviewStatus = ReviewStatus.NEEDS_REVIEW


class AdaptationRecord(StrictModel):
    kind: AdaptationKind
    title_uk: str | None = None
    text_uk: str = Field(min_length=1)
    citations: list[str] = Field(default_factory=list)
    qr_asset: str | None = Field(default=None, pattern=r"^qr_[a-z0-9_]+\.png$")
    status: ReviewStatus = ReviewStatus.NEEDS_REVIEW

    @model_validator(mode="after")
    def historical_notes_need_sources(self) -> AdaptationRecord:
        if self.kind is AdaptationKind.HISTORICAL_NOTE and not self.citations:
            raise ValueError("Historical notes require at least one citation")
        if self.qr_asset and self.kind is not AdaptationKind.INTERACTIVE_LINK:
            raise ValueError("QR assets are supported only for interactive links")
        if self.qr_asset and not self.citations:
            raise ValueError("Interactive links with QR assets require a URL citation")
        return self


class FigureReference(StrictModel):
    id: str
    source_number: int | None = Field(default=None, ge=1)
    source_crop: str | None = None
    vector_source: str | None = None
    alt_uk: str | None = None
    status: ReviewStatus = ReviewStatus.PENDING

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not BLOCK_ID_PATTERN.fullmatch(value):
            raise ValueError("Figure id must be lowercase and stable")
        return value


class AngleMeasure(StrictModel):
    degrees: int = Field(ge=0)
    minutes: int = Field(default=0, ge=0, lt=60)
    seconds: int = Field(default=0, ge=0, lt=60)

    @property
    def total_arcseconds(self) -> int:
        return self.degrees * 3600 + self.minutes * 60 + self.seconds


class AngleSumCheck(StrictModel):
    kind: Literal["angle_sum"]
    measures: list[AngleMeasure] = Field(min_length=2)
    expected: AngleMeasure


class LineRelationCheck(StrictModel):
    kind: Literal["line_relation"]
    relation: Literal["parallel", "perpendicular"]
    points: dict[str, tuple[str, str]]
    line_a: tuple[str, str]
    line_b: tuple[str, str]


MathCheck = Annotated[AngleSumCheck | LineRelationCheck, Field(discriminator="kind")]


class QARecord(StrictModel):
    terminology: ReviewStatus = ReviewStatus.PENDING
    mathematical: ReviewStatus = ReviewStatus.PENDING
    human_review: ReviewStatus = ReviewStatus.PENDING
    notes: list[str] = Field(default_factory=list)


class ContentBlock(StrictModel):
    schema_version: str = "1.0"
    id: str
    kind: BlockKind
    ordinal: str
    title_uk: str
    title_ru: str | None = None
    sources: list[SourceReference] = Field(min_length=1)
    ocr: OCRRecord
    translation: TranslationRecord | None = None
    adaptations: list[AdaptationRecord] = Field(default_factory=list)
    figures: list[FigureReference] = Field(default_factory=list)
    math_checks: list[MathCheck] = Field(default_factory=list)
    qa: QARecord = Field(default_factory=QARecord)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not BLOCK_ID_PATTERN.fullmatch(value):
            raise ValueError("Block id must be lowercase and stable")
        return value
