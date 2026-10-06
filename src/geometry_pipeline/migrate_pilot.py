"""Migrate the legacy angles pilot into small, traceable content blocks."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .schema import ContentBlock

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OCR_PATH = PROJECT_ROOT / "data/geometry/03_ocr_original/section_01_angles.md"
DRAFT_PATH = PROJECT_ROOT / "data/geometry/04_translation_draft/section_01_angles_draft.md"
FINAL_PATH = PROJECT_ROOT / "data/geometry/05_final_edited/section_01_angles_final.md"
INTRO_OCR_PATH = PROJECT_ROOT / "data/geometry/03_ocr_original/introduction.md"
INTRO_FINAL_PATH = PROJECT_ROOT / "data/geometry/05_final_edited/introduction_final.md"
OUTPUT_DIR = PROJECT_ROOT / "book_geometry/content/sections/01_angles"
INTRO_OUTPUT_DIR = PROJECT_ROOT / "book_geometry/content/sections/00_introduction"
QUARANTINE_PATH = PROJECT_ROOT / "data/geometry/review_reports/quarantined_adaptations.jsonl"
SOURCE_PDF = "Kisieliev A.P. - Eliemientarnai - 1931.pdf"

INTRO_PAGE_MAP: dict[int, list[int]] = {
    1: [10],
    2: [10],
    3: [10],
    4: [10, 11],
    5: [11],
    6: [11],
    7: [11, 12],
    8: [12],
    9: [12],
    10: [12, 13],
    11: [13],
    12: [13],
}

INTRO_SLUGS = {
    1: "geometric-figures",
    2: "geometry",
    3: "straight-line",
    4: "line-segment-ray",
    5: "segment-equality",
    6: "segment-sum",
    7: "segment-operations",
    8: "circle-concepts",
    9: "arc-equality",
    10: "arc-sum",
    11: "plane",
    12: "geometry-branches",
}


SECTION_PAGE_MAP: dict[int, list[int]] = {
    13: [14],
    14: [14],
    15: [15],
    16: [15, 16],
    17: [16],
    18: [16, 17],
    19: [17],
    20: [17],
    21: [17, 18],
    22: [18],
    23: [19],
    24: [19],
    25: [19, 20],
    26: [20],
}

SECTION_SLUGS = {
    13: "definition-angle",
    14: "angle-equality",
    15: "angle-sum",
    16: "extended-angles",
    17: "central-angle",
    18: "angle-degrees",
    19: "central-angle-arc",
    20: "protractor",
    21: "angle-types",
    22: "adjacent-angles",
    23: "perpendicular-oblique",
    24: "set-square",
    25: "vertical-angles",
    26: "common-vertex-angles",
}

SECTION_KINDS = {
    13: "definition",
    17: "theorem",
    21: "definition",
    22: "theorem",
    23: "definition",
    25: "theorem",
}

EXERCISE_SLUGS = {
    1: "supplementary-angle",
    2: "straight-line-test",
    3: "construct-bisector",
    4: "adjacent-bisectors",
    5: "vertical-bisectors",
    6: "opposite-rays",
    7: "two-intersecting-lines",
}

FIGURE_VECTOR_MAP = {
    **{number: f"book_geometry/figures/fig-{number:03d}.tex" for number in range(1, 28)},
    14: "book_geometry/figures/fig-014-015.tex",
    15: "book_geometry/figures/fig-014-015.tex",
}

FIGURE_ALT_UK = {
    1: "Пряма AB, позначена також малою літерою a",
    2: "Відрізок CD",
    3: "Промінь із початком у точці A",
    4: "Порівняння відрізків AB і CD",
    5: "Послідовне додавання трьох відрізків",
    6: "Основні елементи кола і круга",
    7: "Додавання дуг однакового радіуса",
    8: "Кут AOB і внутрішні промені OD та OE",
    9: "Порівняння кутів способом накладання",
    10: "Додавання двох кутів",
    11: "Бісектриса кута",
    12: "Розгорнутий кут як сума частин",
    13: "Повний кут навколо точки O",
    14: "Центральний кут",
    15: "Рівні центральні кути й відповідні дуги",
    16: "Вимірювання кута відповідною дугою",
    17: "Вимірювання кута транспортиром",
    18: "Прямий, гострий і тупий кути",
    19: "Суміжні кути",
    20: "Два кути, суміжні з одним кутом",
    21: "Перпендикулярні прямі",
    22: "Похила і перпендикуляр до прямої",
    23: "Побудова перпендикуляра косинцем",
    24: "Вертикальні кути при перетині двох прямих",
    25: "Кути по один бік від прямої",
    26: "Кути навколо спільної вершини",
    27: "Ознака суміжних кутів",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _clean_markdown(text: str) -> str:
    lines = [
        line.rstrip()
        for line in text.strip().splitlines()
        if line.strip() != "---" and not re.match(r"^#{1,3}\s", line)
    ]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def _extract_bold_sections(
    text: str, allowed_numbers: range = range(13, 27)
) -> dict[int, tuple[str, str]]:
    pattern = re.compile(r"(?m)^\*\*(\d{1,3})\.\s*(.+?)\.\*\*\s*")
    matches = list(pattern.finditer(text))
    result: dict[int, tuple[str, str]] = {}
    exercise_start = text.find("### Упражнения")
    if exercise_start < 0:
        exercise_start = text.find("### Вправи")

    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if exercise_start >= 0:
            end = min(end, exercise_start)
        number = int(match.group(1))
        if number in allowed_numbers:
            result[number] = (match.group(2).strip(), _clean_markdown(text[match.end() : end]))
    return result


def _extract_final_sections(text: str) -> dict[int, tuple[str, str]]:
    pattern = re.compile(r"(?m)^### (1[3-9]|2[0-6])\.\s*(.+)$")
    matches = list(pattern.finditer(text))
    result: dict[int, tuple[str, str]] = {}
    exercise_start = text.find("## 4. Вправи")
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else exercise_start
        number = int(match.group(1))
        result[number] = (match.group(2).strip(), _clean_markdown(text[match.end() : end]))
    return result


def _split_adaptations(
    block_id: str, text: str
) -> tuple[str, list[dict[str, object]], list[dict[str, str]]]:
    base_lines: list[str] = []
    quote_groups: list[list[str]] = []
    current_quote: list[str] = []

    def flush_quote() -> None:
        nonlocal current_quote
        if current_quote:
            quote_groups.append(current_quote)
            current_quote = []

    for line in text.splitlines():
        if line.startswith(">"):
            current_quote.append(line.removeprefix(">").lstrip())
        else:
            flush_quote()
            base_lines.append(line)
    flush_quote()

    adaptations: list[dict[str, object]] = []
    quarantine: list[dict[str, str]] = []
    for index, group in enumerate(quote_groups, start=1):
        heading = ""
        body_lines = group
        if group and re.match(r"^#{1,3}\s", group[0]):
            heading = re.sub(r"^#{1,3}\s*", "", group[0]).strip()
            body_lines = group[1:]
        adaptation_text = _clean_markdown("\n".join(body_lines))
        lowered = f"{heading}\n{adaptation_text}".casefold()
        heading_without_trailing_colon = heading.rstrip(":").strip()
        title = (
            heading_without_trailing_colon.split(":", maxsplit=1)[1].strip()
            if ":" in heading_without_trailing_colon
            else None
        )
        if "погляд у майбутнє" in lowered or "вавилон" in lowered:
            quarantine.append(
                {
                    "block_id": block_id,
                    "adaptation_id": f"{block_id}.adaptation-{index}",
                    "reason": "historical_note_requires_sources",
                    "text_uk": adaptation_text,
                }
            )
            continue

        citations = re.findall(r"https?://[^\s)\]]+", adaptation_text)
        if "побачити в русі" in lowered or citations:
            kind = "interactive_link"
        elif "пастка мислення" in lowered:
            kind = "misconception"
        elif "дороговказ" in lowered:
            kind = "proof_guide"
        elif "термінологічна адаптація" in lowered:
            kind = "terminology_adaptation"
        else:
            kind = "editorial_explanation"
        adaptations.append(
            {
                "kind": kind,
                "title_uk": title,
                "text_uk": adaptation_text,
                "citations": sorted(set(citations)),
                "status": "needs_review",
            }
        )

    return _clean_markdown("\n".join(base_lines)), adaptations, quarantine


def _figure_numbers(*texts: str) -> list[int]:
    values: set[int] = set()
    pattern = re.compile(r"\b(?:рис|черт)\.\s*~?\s*(\d+)\b", re.IGNORECASE)
    for text in texts:
        values.update(int(value) for value in pattern.findall(text))
    return sorted(values)


def _source_references(pdf_pages: list[int], section: str) -> list[dict[str, object]]:
    references: list[dict[str, object]] = []
    for pdf_page in pdf_pages:
        image_relative = f"data/geometry/01_raw_pages/page_{pdf_page:03d}_300dpi.png"
        image_path = PROJECT_ROOT / image_relative
        references.append(
            {
                "pdf_path": SOURCE_PDF,
                "pdf_page": pdf_page,
                "printed_page": pdf_page - 1,
                "section": section,
                "source_image": image_relative,
                "image_sha256": _sha256(image_path),
                "bbox": None,
            }
        )
    return references


def _figures(numbers: list[int]) -> list[dict[str, object]]:
    return [
        {
            "id": f"fig-{number:03d}",
            "source_number": number,
            "source_crop": None,
            "vector_source": FIGURE_VECTOR_MAP.get(number),
            "alt_uk": FIGURE_ALT_UK.get(number),
            "status": "needs_review",
        }
        for number in numbers
    ]


def _extract_numbered_list(text: str, heading: str) -> dict[int, str]:
    start = text.index(heading) + len(heading)
    tail = text[start:]
    pattern = re.compile(r"(?m)^([1-7])\.\s+")
    matches = list(pattern.finditer(tail))
    result: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(tail)
        result[int(match.group(1))] = _clean_markdown(tail[match.end() : end])
    return result


def _extract_final_exercises(text: str) -> dict[int, str]:
    pattern = re.compile(r"(?m)^### Вправа ([1-7]) \(Кисельов\)$")
    matches = list(pattern.finditer(text))
    result: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[int(match.group(1))] = _clean_markdown(text[match.end() : end])
    return result


def _exercise_parts(text: str) -> tuple[str, str]:
    condition_match = re.search(
        r"\*Умова:\*\s*(.*?)(?=\n\s*\*(?:Розв'язання|Доведення):\*|\Z)",
        text,
        flags=re.DOTALL,
    )
    if not condition_match:
        raise ValueError("Exercise has no '*Умова:*' section")
    condition = _clean_markdown(condition_match.group(1))
    solution = _clean_markdown(text[condition_match.end() :])
    return condition, solution


def _math_checks(exercise_number: int) -> list[dict[str, object]]:
    if exercise_number == 1:
        return [
            {
                "kind": "angle_sum",
                "measures": [
                    {"degrees": 38, "minutes": 29, "seconds": 0},
                    {"degrees": 141, "minutes": 31, "seconds": 0},
                ],
                "expected": {"degrees": 180, "minutes": 0, "seconds": 0},
            }
        ]
    if exercise_number == 2:
        return [
            {
                "kind": "angle_sum",
                "measures": [
                    {"degrees": 100, "minutes": 20, "seconds": 0},
                    {"degrees": 79, "minutes": 40, "seconds": 0},
                ],
                "expected": {"degrees": 180, "minutes": 0, "seconds": 0},
            }
        ]
    return []


def _write_block(block: ContentBlock, file_name: str, output_dir: Path = OUTPUT_DIR) -> None:
    output_path = output_dir / file_name
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(block.model_dump(mode="json"), ensure_ascii=False, indent=2)
    output_path.write_text(payload + "\n", encoding="utf-8")


def migrate() -> tuple[int, int]:
    ocr_text = OCR_PATH.read_text(encoding="utf-8")
    draft_text = DRAFT_PATH.read_text(encoding="utf-8")
    final_text = FINAL_PATH.read_text(encoding="utf-8")

    source_sections = _extract_bold_sections(ocr_text)
    draft_sections = _extract_bold_sections(draft_text)
    final_sections = _extract_final_sections(final_text)
    quarantine: list[dict[str, str]] = []

    intro_source_sections = _extract_bold_sections(
        INTRO_OCR_PATH.read_text(encoding="utf-8"), range(1, 13)
    )
    intro_final_sections = _extract_bold_sections(
        INTRO_FINAL_PATH.read_text(encoding="utf-8"), range(1, 13)
    )

    for number in range(1, 13):
        title_ru, source_text = intro_source_sections[number]
        title_uk, final_block = intro_final_sections[number]
        printed_page = INTRO_PAGE_MAP[number][0] - 1
        block_id = f"geo.p{printed_page:03d}.s{number:02d}.{INTRO_SLUGS[number]}"
        translation, adaptations, quarantined = _split_adaptations(block_id, final_block)
        quarantine.extend(quarantined)
        figures = _figure_numbers(source_text, translation)
        block = ContentBlock.model_validate(
            {
                "schema_version": "1.0",
                "id": block_id,
                "kind": "definition" if number in {1, 3, 4, 8, 11, 12} else "paragraph",
                "ordinal": str(number),
                "title_uk": title_uk,
                "title_ru": title_ru,
                "sources": _source_references(INTRO_PAGE_MAP[number], "Введение"),
                "ocr": {
                    "text_ru": source_text,
                    "engine": "manual-scan-transcription",
                    "model": None,
                    "prompt_version": "intro-transcription-v1",
                    "run_id": "pilot-2026-09-28",
                    "confidence": None,
                    "status": "needs_review",
                },
                "translation": {
                    "text_uk": translation,
                    "model": None,
                    "prompt_version": "intro-adaptation-v1",
                    "glossary_version": "1.0",
                    "omissions": [],
                    "status": "needs_review",
                },
                "adaptations": adaptations,
                "figures": _figures(figures),
                "math_checks": [],
                "qa": {
                    "terminology": "pending",
                    "mathematical": "pending",
                    "human_review": "needs_review",
                    "notes": [
                        "Вручну транскрибовано зі скану друкованих сторінок 9–12.",
                        "Потребує звірки другим редактором.",
                    ],
                },
            }
        )
        _write_block(block, f"{block_id}.json", INTRO_OUTPUT_DIR)

    for number in range(13, 27):
        title_ru, source_text = source_sections[number]
        _, draft_translation = draft_sections[number]
        title_uk, final_block = final_sections[number]
        printed_page = SECTION_PAGE_MAP[number][0] - 1
        block_id = f"geo.p{printed_page:03d}.s{number}.{SECTION_SLUGS[number]}"
        translation, adaptations, quarantined = _split_adaptations(block_id, final_block)
        quarantine.extend(quarantined)
        figures = _figure_numbers(source_text, draft_translation, translation)

        block = ContentBlock.model_validate(
            {
                "schema_version": "1.0",
                "id": block_id,
                "kind": SECTION_KINDS.get(number, "paragraph"),
                "ordinal": str(number),
                "title_uk": title_uk,
                "title_ru": title_ru,
                "sources": _source_references(SECTION_PAGE_MAP[number], "I. Углы"),
                "ocr": {
                    "text_ru": source_text,
                    "engine": "legacy-markdown-import",
                    "model": None,
                    "prompt_version": "legacy-untracked",
                    "run_id": "pilot-2026-09-28",
                    "confidence": None,
                    "status": "approved",
                },
                "translation": {
                    "text_uk": translation,
                    "model": None,
                    "prompt_version": "legacy-untracked",
                    "glossary_version": "1.0",
                    "omissions": [],
                    "status": "needs_review",
                },
                "adaptations": adaptations,
                "figures": _figures(figures),
                "math_checks": [],
                "qa": {
                    "terminology": "pending",
                    "mathematical": "pending",
                    "human_review": "needs_review",
                    "notes": [
                        "Мігровано автоматично з legacy OCR, draft і final Markdown.",
                        f"Чернетка перекладу містила {len(draft_translation)} символів.",
                    ],
                },
            }
        )
        file_name = f"{block_id}.json"
        _write_block(block, file_name)

    source_exercises = _extract_numbered_list(ocr_text, "### Упражнения")
    draft_exercises = _extract_numbered_list(draft_text, "### Вправи")
    final_exercises = _extract_final_exercises(final_text)

    for number in range(1, 8):
        condition, solution = _exercise_parts(final_exercises[number])
        pdf_page = 20 if number <= 3 else 21
        printed_page = pdf_page - 1
        block_id = f"geo.p{printed_page:03d}.ex{number:02d}.{EXERCISE_SLUGS[number]}"
        figures = _figure_numbers(source_exercises[number], draft_exercises[number], condition)
        adaptations = []
        if solution:
            adaptations.append(
                {
                    "kind": "worked_solution",
                    "title_uk": None,
                    "text_uk": solution,
                    "citations": [],
                    "status": "needs_review",
                }
            )

        block = ContentBlock.model_validate(
            {
                "schema_version": "1.0",
                "id": block_id,
                "kind": "exercise",
                "ordinal": str(number),
                "title_uk": f"Вправа {number}",
                "title_ru": f"Упражнение {number}",
                "sources": _source_references([pdf_page], "I. Углы — упражнения"),
                "ocr": {
                    "text_ru": source_exercises[number],
                    "engine": "legacy-markdown-import",
                    "model": None,
                    "prompt_version": "legacy-untracked",
                    "run_id": "pilot-2026-09-28",
                    "confidence": None,
                    "status": "approved",
                },
                "translation": {
                    "text_uk": condition,
                    "model": None,
                    "prompt_version": "legacy-untracked",
                    "glossary_version": "1.0",
                    "omissions": [],
                    "status": "needs_review",
                },
                "adaptations": adaptations,
                "figures": _figures(figures),
                "math_checks": _math_checks(number),
                "qa": {
                    "terminology": "pending",
                    "mathematical": "pending",
                    "human_review": "needs_review",
                    "notes": ["Мігровано автоматично з legacy Markdown."],
                },
            }
        )
        _write_block(block, f"{block_id}.json")

    QUARANTINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    quarantine_payload = "\n".join(
        json.dumps(item, ensure_ascii=False, sort_keys=True) for item in quarantine
    )
    QUARANTINE_PATH.write_text(
        quarantine_payload + ("\n" if quarantine_payload else ""), encoding="utf-8"
    )
    return 33, len(quarantine)


def main() -> int:
    blocks, quarantined = migrate()
    print(f"Migrated {blocks} blocks; quarantined {quarantined} adaptations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
