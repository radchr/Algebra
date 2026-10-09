"""Lesson loader: clean Markdown lessons -> renderable segments.

Уроки живуть у ``content/geometry/*.md`` і є єдиним джерелом тексту.
Окрім звичайного Markdown, підтримуються три службові конструкції:

* ``::: feynman Заголовок`` … ``:::`` — блок «Інтуїція Фейнмана»;
* ``::: misconception Заголовок`` … ``:::`` — блок «Пастка мислення»;
* ``<!-- figure: N -->`` — готовий рисунок N із ``book_kb.db``;
* ``<!-- widget: name -->`` — живий віджет застосунку (див. ``KNOWN_WIDGETS``).

HTML-коментарі невидимі в будь-якому переглядачі Markdown, тож файли
лишаються чистими й людинозчитуваними. Модуль не залежить від marimo.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .db import BookDatabase

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LESSONS_DIR = PROJECT_ROOT / "content" / "geometry"

# kind -> (іконка, CSS-клас)
BOX_STYLES: dict[str, tuple[str, str]] = {
    "feynman": ("🧠", "feynman-box"),
    "misconception": ("⚠️", "misconception-box"),
}

# Віджети, які вміє будувати app_geometry.py
KNOWN_WIDGETS: frozenset[str] = frozenset(
    {
        "segment_addition",
        "angle_rotation",
        "angle_bisector",
        "adjacent_angles",
        "vertical_scissors",
        "congruence_criteria",
        "triangle_superposition",
    }
)

SegmentKind = Literal["markdown", "box", "figure", "widget"]

_FIGURE_RE = re.compile(r"<!--\s*figure:\s*(\d+)\s*-->")
_WIDGET_RE = re.compile(r"<!--\s*widget:\s*([a-z_]+)\s*-->")
_SOURCE_PAGES_RE = re.compile(r"<!--\s*source-pages:\s*(\d+)\s*-\s*(\d+)\s*-->")
_BOX_OPEN_RE = re.compile(r":::\s*(\w+)\s*(.*)")
_BOX_CLOSE = ":::"


class LessonFormatError(ValueError):
    """Помилка структури уроку (незакритий блок, невідомий віджет тощо)."""


@dataclass(frozen=True)
class Segment:
    kind: SegmentKind
    text: str = ""  # Markdown-тіло (markdown / box)
    box: str = ""  # feynman | misconception
    title: str = ""  # заголовок блоку
    fig_num: int = 0  # номер рисунка
    widget: str = ""  # назва віджета

    def box_markdown(self) -> str:
        """Markdown блоку разом із заголовком та іконкою."""
        icon, _ = BOX_STYLES[self.box]
        return f"**{icon} {self.title}**\n\n{self.text}" if self.title else self.text

    @property
    def css_class(self) -> str:
        return BOX_STYLES[self.box][1] if self.kind == "box" else ""


@dataclass(frozen=True)
class Lesson:
    lesson_id: str
    title: str
    segments: tuple[Segment, ...]
    source_pages: tuple[int, ...]

    @property
    def figure_refs(self) -> list[int]:
        return [s.fig_num for s in self.segments if s.kind == "figure"]

    @property
    def widget_refs(self) -> list[str]:
        return [s.widget for s in self.segments if s.kind == "widget"]


def parse_lesson(text: str) -> list[Segment]:
    """Розбирає текст уроку на послідовність сегментів."""
    segments: list[Segment] = []
    buffer: list[str] = []

    def flush() -> None:
        markdown = "\n".join(buffer).strip()
        if markdown:
            segments.append(Segment("markdown", text=markdown))
        buffer.clear()

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if _SOURCE_PAGES_RE.fullmatch(stripped):
            flush()
        elif m := _FIGURE_RE.fullmatch(stripped):
            flush()
            segments.append(Segment("figure", fig_num=int(m.group(1))))
        elif m := _WIDGET_RE.fullmatch(stripped):
            name = m.group(1)
            if name not in KNOWN_WIDGETS:
                raise LessonFormatError(f"Рядок {i + 1}: невідомий віджет «{name}»")
            flush()
            segments.append(Segment("widget", widget=name))
        elif stripped == _BOX_CLOSE:
            raise LessonFormatError(f"Рядок {i + 1}: «:::» без відкриваючого блоку")
        elif m := _BOX_OPEN_RE.fullmatch(stripped):
            kind, title = m.group(1), m.group(2).strip()
            if kind not in BOX_STYLES:
                raise LessonFormatError(f"Рядок {i + 1}: невідомий тип блоку «{kind}»")
            flush()
            start = i
            body: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() != _BOX_CLOSE:
                body.append(lines[i])
                i += 1
            if i == len(lines):
                raise LessonFormatError(f"Рядок {start + 1}: блок «::: {kind}» не закрито")
            segments.append(Segment("box", text="\n".join(body).strip(), box=kind, title=title))
        else:
            buffer.append(line)
        i += 1

    flush()
    return segments


def _extract_title(segments: list[Segment], fallback: str) -> tuple[str, list[Segment]]:
    """Забирає H1 з першого Markdown-сегмента як назву уроку."""
    if segments and segments[0].kind == "markdown":
        first, *rest = segments[0].text.split("\n", 1)
        if first.startswith("# "):
            remaining = rest[0].strip() if rest else ""
            # Горизонтальна лінія одразу після заголовка не потрібна у застосунку
            remaining = re.sub(r"^-{3,}\s*", "", remaining).strip()
            tail = [Segment("markdown", text=remaining)] if remaining else []
            return first[2:].strip(), tail + segments[1:]
    return fallback, segments


def lesson_paths(lessons_dir: Path = LESSONS_DIR) -> list[Path]:
    return sorted(lessons_dir.glob("[0-9][0-9]_*.md"))


def load_lesson(path: Path) -> Lesson:
    text = path.read_text(encoding="utf-8")
    source_matches = _SOURCE_PAGES_RE.findall(text)
    if len(source_matches) != 1:
        raise LessonFormatError(f"{path.name}: потрібна одна мітка <!-- source-pages: N-M -->")
    first_page, last_page = (int(value) for value in source_matches[0])
    if first_page > last_page:
        raise LessonFormatError(f"{path.name}: некоректний діапазон source-pages")
    segments = parse_lesson(text)
    title, segments = _extract_title(segments, fallback=path.stem)
    return Lesson(
        lesson_id=path.stem,
        title=title,
        segments=tuple(segments),
        source_pages=tuple(range(first_page, last_page + 1)),
    )


def load_all_lessons(
    lessons_dir: Path = LESSONS_DIR,
    *,
    require_verified_cache: bool = True,
    database: BookDatabase | None = None,
    book_id: str = "kiselev_geometry_1931",
) -> list[Lesson]:
    lessons = [load_lesson(p) for p in lesson_paths(lessons_dir)]
    if require_verified_cache:
        db = database or BookDatabase()
        for lesson in lessons:
            db.require_verified_pages(book_id, lesson.source_pages)
    return lessons
