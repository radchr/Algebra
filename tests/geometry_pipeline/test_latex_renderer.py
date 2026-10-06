from pathlib import Path

from geometry_pipeline.latex_renderer import (
    load_blocks,
    markdown_to_latex,
    render_introduction,
    render_section,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTENT_ROOT = PROJECT_ROOT / "book_geometry/content/sections/01_angles"
ALL_CONTENT_ROOT = PROJECT_ROOT / "book_geometry/content/sections"


def test_markdown_renderer_preserves_math_and_converts_styles() -> None:
    source = "1. **Сума:** $a_b + c = 180^\\circ$.\n2. *Висновок.*"
    rendered = markdown_to_latex(source)

    assert r"\begin{enumerate}" in rendered
    assert r"\textbf{Сума:}" in rendered
    assert r"$a_b + c = 180^\circ$" in rendered
    assert r"\emph{Висновок.}" in rendered
    assert rendered.count(r"\begin{enumerate}") == 1


def test_complete_pilot_renders_all_blocks_in_book_order() -> None:
    blocks = load_blocks(CONTENT_ROOT)
    rendered = render_section(blocks)

    assert len(blocks) == 21
    assert rendered.count("% block:") == 21
    assert rendered.index("13. Кут.") < rendered.index("26. Кути")
    assert rendered.index("26. Кути") < rendered.index("Вправа 1")
    assert "## 3." not in rendered
    assert "Місце для реконструкції" not in rendered
    assert r"\input{figures/fig-008.tex}" in rendered
    assert r"\begin{warningbox}[Розгорнутий кут" in rendered
    assert r"\begin{scaffoldbox}[Властивість суміжних кутів]" in rendered
    assert r"\begin{mediabox}[Побачити через рух: кут як поворот]" in rendered
    assert rendered.count(r"\begin{mediabox}[Побачити через рух:") == 6


def test_introduction_precedes_angles_and_has_all_source_blocks() -> None:
    blocks = load_blocks(ALL_CONTENT_ROOT)
    rendered = render_introduction(blocks)

    assert len(blocks) == 33
    assert rendered.count("% block:") == 12
    assert rendered.index("1. Геометричні фігури.") < rendered.index("12. Поділ геометрії.")
    assert "Місце для реконструкції" not in rendered
