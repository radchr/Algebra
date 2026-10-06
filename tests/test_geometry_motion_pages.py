from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BOOK = ROOT / "book_geometry"

PAGES = {
    "geometry-angle-rotation.html": "angle-rotation",
    "geometry-central-angle-arc.html": "central-angle-arc",
    "geometry-adjacent-angles.html": "adjacent-angles",
    "geometry-vertical-half-turn.html": "vertical-half-turn",
    "geometry-adjacent-bisectors.html": "adjacent-bisectors",
    "geometry-vertical-bisectors.html": "vertical-bisectors",
    "geometry-point-trace.html": "point-trace",
    "geometry-circle-trace.html": "circle-trace",
    "geometry-equal-angles-motion.html": "equal-angles-motion",
}

NEW_PAGES = {
    "geometry-point-trace.html": "js/geometry/point-trace.js",
    "geometry-circle-trace.html": "js/geometry/circle-trace.js",
    "geometry-equal-angles-motion.html": "js/geometry/equal-angles-motion.js",
}


def test_each_motion_fact_has_a_standalone_page() -> None:
    for filename, demo in PAGES.items():
        text = (DOCS / filename).read_text(encoding="utf-8")
        assert f'data-demo="{demo}"' in text
        assert 'id="motion-stage"' in text
        assert 'id="motion-slider"' in text
        assert text.count('class="motion-card"') == 1

        if filename in NEW_PAGES:
            assert NEW_PAGES[filename] in text
            assert 'id="prediction-form"' in text
            assert 'class="motion-mission"' in text
        else:
            assert "geometry-motion.js" in text


def test_pdf_links_to_every_motion_page_and_qr_asset() -> None:
    section = (BOOK / "sections" / "section_01_angles.tex").read_text(encoding="utf-8")
    introduction_blocks = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (BOOK / "content" / "sections" / "00_introduction").glob("*.json")
    )
    for filename in PAGES:
        if filename in {"geometry-point-trace.html", "geometry-circle-trace.html"}:
            assert f"https://radchr.github.io/Algebra/{filename}" in introduction_blocks
            continue
        assert f"https://radchr.github.io/Algebra/{filename}" in section

    qr_files = {
        "qr_angle_rotation.png",
        "qr_central_angle_arc.png",
        "qr_adjacent_angles.png",
        "qr_vertical_half_turn.png",
        "qr_adjacent_bisectors.png",
        "qr_vertical_bisectors.png",
        "qr_point_trace.png",
        "qr_circle_trace.png",
        "qr_equal_angles_motion.png",
    }
    for filename in qr_files:
        assert (BOOK / filename).is_file()
        assert (BOOK / filename).stat().st_size > 500
        if filename in {"qr_point_trace.png", "qr_circle_trace.png"}:
            assert filename in introduction_blocks
        else:
            assert filename in section


def test_structured_content_uses_the_standalone_urls() -> None:
    found_urls: set[str] = set()
    for path in (BOOK / "content" / "sections").rglob("*.json"):
        block = json.loads(path.read_text(encoding="utf-8"))
        for adaptation in block.get("adaptations", []):
            if adaptation.get("kind") == "interactive_link":
                found_urls.update(adaptation.get("citations", []))

    expected = {f"https://radchr.github.io/Algebra/{filename}" for filename in PAGES}
    assert expected <= found_urls


def test_new_motion_modules_share_the_svg_core() -> None:
    core = DOCS / "js" / "geometry" / "core.js"
    assert core.is_file()
    assert "export const createScene" in core.read_text(encoding="utf-8")
    for script in NEW_PAGES.values():
        text = (DOCS / script).read_text(encoding="utf-8")
        assert 'from "./core.js"' in text
        assert "setSvgSummary" in text


def test_every_github_pages_book_link_has_a_deployed_file() -> None:
    """A QR/link in the PDF must resolve to a file shipped from docs/."""
    sources = [
        BOOK / "main.tex",
        *sorted((BOOK / "sections").glob("*.tex")),
        *sorted((BOOK / "generated" / "sections").glob("*.tex")),
        *sorted((BOOK / "content" / "sections").rglob("*.json")),
    ]
    prefix = "https://radchr.github.io/Algebra/"
    deployed_paths: set[str] = set()

    for source in sources:
        text = source.read_text(encoding="utf-8")
        deployed_paths.update(
            match.rstrip("%,.;")
            for match in re.findall(
                rf"{re.escape(prefix)}[^\s<>{{}}\[\]\\\"')]+",
                text,
            )
        )

    assert deployed_paths
    for url in deployed_paths:
        relative_path = url.removeprefix(prefix)
        assert (DOCS / relative_path).is_file(), f"Missing GitHub Pages file for {url}"
