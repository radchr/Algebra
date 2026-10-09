"""Tests for lesson parsing, cache integrity, safe answer parsing and the Marimo app."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from geometry_engine.db import DB_PATH, BookDatabase, BookFigure, BookPage
from geometry_engine.lesson import (
    KNOWN_WIDGETS,
    LessonFormatError,
    load_all_lessons,
    load_lesson,
    parse_lesson,
)
from geometry_engine.svg_drawings import get_book_figure
from geometry_engine.sympy_solver import (
    parse_math_input,
    verify_adjacent_angle,
    verify_congruence_mission,
    verify_segment_addition,
)
from geometry_engine.tasks import TASKS

PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------- lesson parser


def test_parse_lesson_segments():
    text = "\n".join(
        [
            "# Заголовок",
            "",
            "Абзац тексту.",
            "<!-- figure: 8 -->",
            "::: feynman Інтуїція",
            "Тіло блоку з $\\angle A$.",
            ":::",
            "<!-- widget: angle_rotation -->",
            "Кінець.",
        ]
    )
    segs = parse_lesson(text)
    assert [s.kind for s in segs] == ["markdown", "figure", "box", "widget", "markdown"]
    assert segs[1].fig_num == 8
    assert segs[2].box == "feynman" and segs[2].title == "Інтуїція"
    assert segs[2].css_class == "feynman-box"
    assert "🧠 Інтуїція" in segs[2].box_markdown()
    assert segs[3].widget == "angle_rotation"


@pytest.mark.parametrize(
    "bad",
    [
        "::: feynman Без кінця\nтекст",
        "текст\n:::\n",
        "::: unknown Х\nтекст\n:::",
        "<!-- widget: no_such_widget -->",
    ],
)
def test_parse_lesson_rejects_broken_structure(bad):
    with pytest.raises(LessonFormatError):
        parse_lesson(bad)


def test_all_lessons_load_with_titles():
    lessons = load_all_lessons(require_verified_cache=False)
    assert len(lessons) >= 3
    for lesson in lessons:
        assert lesson.title and not lesson.title.startswith("#")
        assert lesson.segments


def test_active_lessons_declare_literal_source_pages():
    lessons = {
        lesson.lesson_id: lesson for lesson in load_all_lessons(require_verified_cache=False)
    }
    assert lessons["00_introduction"].source_pages == (9, 10, 11, 12)
    assert lessons["01_angles"].source_pages == tuple(range(13, 21))
    assert lessons["02_triangles_equality"].source_pages == tuple(range(21, 29))


def test_active_lesson_pages_are_verified_and_pedagogically_populated():
    db = BookDatabase()
    lessons = load_all_lessons(require_verified_cache=False)
    for lesson in lessons:
        db.require_verified_pages("kiselev_geometry_1931", lesson.source_pages)
        for page_num in lesson.source_pages:
            page = db.get_page("kiselev_geometry_1931", page_num)
            assert page is not None
            assert page.feynman_notes.strip(), f"стор. {page_num}: немає інтуїції Фейнмана"
            assert page.misconceptions.strip(), f"стор. {page_num}: немає пастки мислення"


def test_active_lessons_cover_their_literal_section_ranges():
    expected = {
        "00_introduction": set(range(1, 13)),
        "01_angles": set(range(13, 27)),
        "02_triangles_equality": set(range(30, 39)),
    }
    for path in sorted((PROJECT_ROOT / "content" / "geometry").glob("[0-9][0-9]_*.md")):
        section_numbers = {
            int(value)
            for value in re.findall(r"^###\s+(\d+)", path.read_text(encoding="utf-8"), re.MULTILINE)
        }
        assert section_numbers == expected[path.stem]


def test_active_lessons_reference_every_figure_from_their_source_pages():
    db = BookDatabase()
    figures = db.list_figures()
    for lesson in load_all_lessons():
        expected = {figure.fig_num for figure in figures if figure.page_num in lesson.source_pages}
        assert set(lesson.figure_refs) == expected


def test_active_page_figure_json_matches_cached_rows():
    db = BookDatabase()
    active_pages = {page_num for lesson in load_all_lessons() for page_num in lesson.source_pages}
    for page_num in active_pages:
        page = db.get_page("kiselev_geometry_1931", page_num)
        assert page is not None
        declared = set(json.loads(page.figures_json))
        actual = {
            figure.fig_id for figure in db.get_figures_for_page("kiselev_geometry_1931", page_num)
        }
        assert declared == actual


def test_lesson_figure_refs_exist_in_cache():
    """Phase 2 rule: every referenced figure must already be in book_kb.db."""
    for lesson in load_all_lessons(require_verified_cache=False):
        for num in lesson.figure_refs:
            fig = get_book_figure(num)
            assert fig is not None, f"{lesson.lesson_id}: рис. {num} відсутній у book_kb.db"
            ET.fromstring(fig.svg_content.encode("utf-8"))  # valid XML


def test_lesson_widget_refs_are_known_and_every_lesson_has_a_task():
    for lesson in load_all_lessons(require_verified_cache=False):
        assert set(lesson.widget_refs) <= KNOWN_WIDGETS
        assert lesson.lesson_id in TASKS, f"немає задачі «Перевір себе» для {lesson.lesson_id}"


# ---------------------------------------------------------------- database


def test_book_page_default_status_is_not_verified():
    page = BookPage(
        book_id="b",
        page_num=1,
        pdf_page=1,
        sections_covered="§ 1",
        ocr_ru="текст",
        translation_uk="текст",
    )
    assert page.status == "translated"


def test_page_readiness_reports_verified_translated_and_missing(tmp_path):
    db = BookDatabase(tmp_path / "kb.db")
    for page_num, status in [(1, "verified"), (2, "translated")]:
        db.save_page(
            BookPage(
                book_id="b",
                page_num=page_num,
                pdf_page=page_num,
                sections_covered=f"§ {page_num}",
                ocr_ru="текст",
                translation_uk="текст",
                status=status,
            )
        )

    assert db.page_readiness("b", [1, 2, 3]) == {
        1: "verified",
        2: "translated",
        3: "missing",
    }
    with pytest.raises(ValueError, match=r"2 \(translated\).+3 \(missing\)"):
        db.require_verified_pages("b", [1, 2, 3])


def test_lesson_declares_source_page_range(tmp_path):
    path = tmp_path / "03_sample.md"
    path.write_text(
        "# Пробний урок\n\n<!-- source-pages: 21-25 -->\n\nТекст уроку.",
        encoding="utf-8",
    )
    lesson = load_lesson(path)
    assert lesson.source_pages == (21, 22, 23, 24, 25)
    assert "source-pages" not in "\n".join(segment.text for segment in lesson.segments)


def test_lesson_rejects_missing_source_pages(tmp_path):
    path = tmp_path / "03_sample.md"
    path.write_text("# Пробний урок\n\nТекст уроку.", encoding="utf-8")
    with pytest.raises(LessonFormatError, match="source-pages"):
        load_lesson(path)


def test_db_path_is_absolute_and_present():
    assert DB_PATH.is_absolute()
    assert DB_PATH.exists()
    assert DB_PATH == PROJECT_ROOT / "data" / "geometry" / "book_kb.db"


def test_book_database_roundtrip(tmp_path):
    db = BookDatabase(tmp_path / "kb.db")
    db.save_page(
        BookPage(
            book_id="b",
            page_num=1,
            pdf_page=3,
            sections_covered="§ 1",
            ocr_ru="текст",
            translation_uk="текст",
        )
    )
    db.save_figure(
        BookFigure(fig_id="f1", fig_num=1, book_id="b", page_num=1, title="T", svg_content="<svg/>")
    )
    assert db.get_page("b", 1).pdf_page == 3
    assert db.count_pages("b") == 1
    assert db.get_figure_by_num("b", 1).title == "T"
    assert db.get_figure("missing") is None
    assert [f.fig_id for f in db.get_figures_for_page("b", 1)] == ["f1"]


def test_all_cached_figures_are_valid_svg():
    for fig in BookDatabase().list_figures():
        root = ET.fromstring(fig.svg_content.encode("utf-8"))
        assert root.tag.endswith("svg"), fig.fig_id


# ---------------------------------------------------------------- safe answer parsing


@pytest.mark.parametrize(
    "raw",
    [
        "abc",
        "x",
        "__import__('os')",
        "1/0",
        "",
        "   ",
        "2**",
        "exp(1)",
        "lambda: 1",
        "(-1)^(1/2)",
    ],
)
def test_parse_math_input_rejects_non_numeric(raw):
    assert parse_math_input(raw) is None


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("7,2 см", "36/5"), ("138°", "138"), ("180 − 42", "138"), ("2^3", "8"), ("3 × 4", "12")],
)
def test_parse_math_input_accepts_school_notation(raw, expected):
    import sympy as sp

    assert parse_math_input(raw) == sp.Rational(expected)


def test_verifiers_never_crash_on_garbage():
    for raw in ["abc", "x + 1", "1/0", "()", "😀", "(-1)^(1/2)"]:
        assert verify_congruence_mission("B₁C₁", 7.2, raw)["correct"] is False
        assert verify_congruence_mission("B₁C₁", 7.2, "7.2", "∠B₁", 60, raw)["correct"] is False
        assert verify_adjacent_angle(42, raw)["correct"] is False
        assert verify_segment_addition(4.5, 3.2, 2.8, raw)["correct"] is False


def test_exact_comparison_has_no_float_noise():
    # 4.5 + 3.2 + 2.8 у float дає 10.500000000000002; точна арифметика — рівно 21/2
    assert verify_segment_addition(4.5, 3.2, 2.8, "10,5")["correct"] is True
    assert verify_segment_addition(4.5, 3.2, 2.8, "10.5000001")["correct"] is False
    assert verify_congruence_mission("B₁C₁", 7.2, "7,2 см")["correct"] is True


def test_tasks_accept_their_own_reference_answers():
    answers = {"00_introduction": "10,5", "01_angles": "138", "02_triangles_equality": "10"}
    for lesson_id, answer in answers.items():
        assert TASKS[lesson_id].check(answer)["correct"] is True
        assert TASKS[lesson_id].check("0")["correct"] is False


def test_triangle_task_uses_a_sympy_verified_reference_answer():
    task = TASKS["02_triangles_equality"]

    assert task.reference_answer == 10
    assert task.check("10")["correct"] is True
    assert task.check("7,2")["correct"] is False


def test_every_task_has_complete_predict_and_three_level_scaffolding():
    for task in TASKS.values():
        assert task.prediction_prompt.strip()
        assert 3 <= len(task.prediction_options) <= 4
        assert task.prediction_answer in task.prediction_options.values()
        assert task.prediction_explanation.strip()
        assert len(task.hints) == 3
        assert all(hint.strip() for hint in task.hints)
        assert len({hint.strip() for hint in task.hints}) == 3


# ---------------------------------------------------------------- marimo app smoke test


def test_app_geometry_runs_headless():
    """All cells of app_geometry.py execute without errors in script mode."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("app_geometry", PROJECT_ROOT / "app_geometry.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _outputs, defs = module.app.run()
    assert set(defs["widgets"]) == KNOWN_WIDGETS
    assert defs["lesson"].lesson_id == "00_introduction"
    assert defs["prediction"].value is None
    assert defs["observation_unlocked"] is False
