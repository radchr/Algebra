"""Database Cache-First Manager for Kiselev Books Knowledge Base.

Stores OCR, NUSH Ukrainian translation, pedagogical blocks, and metadata
in a local SQLite database (data/geometry/book_kb.db).
Guarantees zero redundant VLM API calls.
"""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "geometry" / "book_kb.db"


@dataclass
class BookPage:
    book_id: str
    page_num: int
    pdf_page: int
    sections_covered: str
    ocr_ru: str
    translation_uk: str
    feynman_notes: str = ""
    misconceptions: str = ""
    figures_json: str = "[]"
    status: str = "translated"  # raw | translated | verified
    sha256: str = ""
    updated_at: str = ""


@dataclass
class BookFigure:
    fig_id: str
    fig_num: int
    book_id: str
    page_num: int
    title: str
    section_ref: str = ""
    caption_original: str = ""
    didactic_notes: str = ""
    svg_content: str = ""
    width: int = 360
    height: int = 220
    created_at: str = ""


class BookDatabase:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _get_conn(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            with conn:  # commit on success, rollback on error
                yield conn
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS book_pages (
                    book_id TEXT NOT NULL,
                    page_num INTEGER NOT NULL,
                    pdf_page INTEGER NOT NULL,
                    sections_covered TEXT,
                    ocr_ru TEXT,
                    translation_uk TEXT,
                    feynman_notes TEXT,
                    misconceptions TEXT,
                    figures_json TEXT,
                    status TEXT DEFAULT 'translated',
                    sha256 TEXT,
                    updated_at TEXT,
                    PRIMARY KEY (book_id, page_num)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_book_page
                ON book_pages(book_id, page_num)
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS book_figures (
                    fig_id TEXT PRIMARY KEY,
                    fig_num INTEGER NOT NULL,
                    book_id TEXT NOT NULL,
                    page_num INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    section_ref TEXT,
                    caption_original TEXT,
                    didactic_notes TEXT,
                    svg_content TEXT NOT NULL,
                    width INTEGER DEFAULT 360,
                    height INTEGER DEFAULT 220,
                    created_at TEXT
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_figure_book_num
                ON book_figures(book_id, fig_num)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_figure_page
                ON book_figures(book_id, page_num)
            """)
            conn.commit()

    def has_page(self, book_id: str, page_num: int) -> bool:
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT 1 FROM book_pages WHERE book_id = ? AND page_num = ?",
                (book_id, page_num),
            )
            return cur.fetchone() is not None

    def get_page(self, book_id: str, page_num: int) -> BookPage | None:
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT * FROM book_pages WHERE book_id = ? AND page_num = ?",
                (book_id, page_num),
            )
            row = cur.fetchone()
            if not row:
                return None
            return BookPage(
                book_id=row["book_id"],
                page_num=row["page_num"],
                pdf_page=row["pdf_page"],
                sections_covered=row["sections_covered"] or "",
                ocr_ru=row["ocr_ru"] or "",
                translation_uk=row["translation_uk"] or "",
                feynman_notes=row["feynman_notes"] or "",
                misconceptions=row["misconceptions"] or "",
                figures_json=row["figures_json"] or "[]",
                status=row["status"] or "translated",
                sha256=row["sha256"] or "",
                updated_at=row["updated_at"] or "",
            )

    def save_page(self, page: BookPage) -> None:
        now = datetime.now().isoformat()
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO book_pages (
                    book_id, page_num, pdf_page, sections_covered,
                    ocr_ru, translation_uk, feynman_notes, misconceptions,
                    figures_json, status, sha256, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(book_id, page_num) DO UPDATE SET
                    pdf_page=excluded.pdf_page,
                    sections_covered=excluded.sections_covered,
                    ocr_ru=excluded.ocr_ru,
                    translation_uk=excluded.translation_uk,
                    feynman_notes=excluded.feynman_notes,
                    misconceptions=excluded.misconceptions,
                    figures_json=excluded.figures_json,
                    status=excluded.status,
                    sha256=excluded.sha256,
                    updated_at=excluded.updated_at
            """,
                (
                    page.book_id,
                    page.page_num,
                    page.pdf_page,
                    page.sections_covered,
                    page.ocr_ru,
                    page.translation_uk,
                    page.feynman_notes,
                    page.misconceptions,
                    page.figures_json,
                    page.status,
                    page.sha256,
                    now,
                ),
            )
            conn.commit()

    def list_pages(self, book_id: str) -> list[int]:
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT page_num FROM book_pages WHERE book_id = ? ORDER BY page_num ASC",
                (book_id,),
            )
            return [row["page_num"] for row in cur.fetchall()]

    def count_pages(self, book_id: str) -> int:
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT COUNT(*) as cnt FROM book_pages WHERE book_id = ?",
                (book_id,),
            )
            return cur.fetchone()["cnt"]

    def page_readiness(
        self, book_id: str, page_nums: list[int] | tuple[int, ...]
    ) -> dict[int, str]:
        """Return ``verified``, the stored status, or ``missing`` for every requested page."""
        ordered_pages = tuple(dict.fromkeys(page_nums))
        if not ordered_pages:
            return {}
        placeholders = ", ".join("?" for _ in ordered_pages)
        with self._get_conn() as conn:
            rows = conn.execute(
                f"SELECT page_num, status FROM book_pages "
                f"WHERE book_id = ? AND page_num IN ({placeholders})",
                (book_id, *ordered_pages),
            ).fetchall()
        stored = {row["page_num"]: row["status"] or "translated" for row in rows}
        return {page_num: stored.get(page_num, "missing") for page_num in ordered_pages}

    def require_verified_pages(self, book_id: str, page_nums: list[int] | tuple[int, ...]) -> None:
        """Reject lesson composition until every source page is present and verified."""
        readiness = self.page_readiness(book_id, page_nums)
        problems = [
            f"{page_num} ({status})"
            for page_num, status in readiness.items()
            if status != "verified"
        ]
        if problems:
            raise ValueError(f"Кеш не готовий: {', '.join(problems)}")

    def save_figure(self, figure: BookFigure) -> None:
        now = datetime.now().isoformat()
        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO book_figures (
                    fig_id, fig_num, book_id, page_num, title,
                    section_ref, caption_original, didactic_notes,
                    svg_content, width, height, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(fig_id) DO UPDATE SET
                    fig_num=excluded.fig_num,
                    book_id=excluded.book_id,
                    page_num=excluded.page_num,
                    title=excluded.title,
                    section_ref=excluded.section_ref,
                    caption_original=excluded.caption_original,
                    didactic_notes=excluded.didactic_notes,
                    svg_content=excluded.svg_content,
                    width=excluded.width,
                    height=excluded.height,
                    created_at=excluded.created_at
            """,
                (
                    figure.fig_id,
                    figure.fig_num,
                    figure.book_id,
                    figure.page_num,
                    figure.title,
                    figure.section_ref,
                    figure.caption_original,
                    figure.didactic_notes,
                    figure.svg_content,
                    figure.width,
                    figure.height,
                    now,
                ),
            )
            conn.commit()

    @staticmethod
    def _row_to_figure(row: sqlite3.Row) -> BookFigure:
        return BookFigure(
            fig_id=row["fig_id"],
            fig_num=row["fig_num"],
            book_id=row["book_id"],
            page_num=row["page_num"],
            title=row["title"],
            section_ref=row["section_ref"] or "",
            caption_original=row["caption_original"] or "",
            didactic_notes=row["didactic_notes"] or "",
            svg_content=row["svg_content"],
            width=row["width"],
            height=row["height"],
            created_at=row["created_at"] or "",
        )

    def _query_figures(self, sql: str, params: tuple[Any, ...]) -> list[BookFigure]:
        with self._get_conn() as conn:
            return [self._row_to_figure(row) for row in conn.execute(sql, params).fetchall()]

    def get_figure(self, fig_id: str) -> BookFigure | None:
        found = self._query_figures("SELECT * FROM book_figures WHERE fig_id = ?", (fig_id,))
        return found[0] if found else None

    def get_figure_by_num(self, book_id: str, fig_num: int) -> BookFigure | None:
        found = self._query_figures(
            "SELECT * FROM book_figures WHERE book_id = ? AND fig_num = ?",
            (book_id, fig_num),
        )
        return found[0] if found else None

    def get_figures_for_page(self, book_id: str, page_num: int) -> list[BookFigure]:
        return self._query_figures(
            "SELECT * FROM book_figures WHERE book_id = ? AND page_num = ? ORDER BY fig_num ASC",
            (book_id, page_num),
        )

    def list_figures(self, book_id: str = "kiselev_geometry_1931") -> list[BookFigure]:
        return self._query_figures(
            "SELECT * FROM book_figures WHERE book_id = ? ORDER BY fig_num ASC",
            (book_id,),
        )

    def count_figures(self, book_id: str = "kiselev_geometry_1931") -> int:
        with self._get_conn() as conn:
            cur = conn.execute(
                "SELECT COUNT(*) as cnt FROM book_figures WHERE book_id = ?",
                (book_id,),
            )
            return cur.fetchone()["cnt"]

    def seed_from_existing_json_blocks(self, content_root: Path) -> int:
        """Seeds SQLite database from already verified JSON blocks in book_geometry/content."""
        if not content_root.exists():
            return 0

        seeded_count = 0
        json_files = sorted(content_root.glob("**/*.json"))
        pages_dict: dict[int, dict[str, Any]] = {}

        for jf in json_files:
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
            except Exception:
                continue

            sources = data.get("sources", [{}])
            src = sources[0] if sources else {}
            printed_page = src.get("printed_page", 0)
            pdf_page = src.get("pdf_page", printed_page)

            if not printed_page:
                continue

            if printed_page not in pages_dict:
                pages_dict[printed_page] = {
                    "book_id": "kiselev_geometry_1931",
                    "page_num": printed_page,
                    "pdf_page": pdf_page,
                    "sections": [],
                    "ocr_parts": [],
                    "trans_parts": [],
                    "feynman_parts": [],
                    "figures": [],
                }

            record = pages_dict[printed_page]
            title = data.get("title_uk", "")
            ordinal = data.get("ordinal", "")
            if ordinal:
                record["sections"].append(f"§ {ordinal} {title}")

            ocr_txt = data.get("ocr", {}).get("text_ru", "")
            if ocr_txt:
                record["ocr_parts"].append(ocr_txt)

            trans_txt = data.get("translation", {}).get("text_uk", "")
            if trans_txt:
                record["trans_parts"].append(trans_txt)

            for adapt in data.get("adaptations", []):
                if adapt.get("kind") == "editorial_explanation":
                    record["feynman_parts"].append(
                        f"**{adapt.get('title_uk', '')}**\n{adapt.get('text_uk', '')}"
                    )

            for fig in data.get("figures", []):
                record["figures"].append(fig.get("id", ""))

        for page_num, rec in pages_dict.items():
            bp = BookPage(
                book_id=rec["book_id"],
                page_num=page_num,
                pdf_page=rec["pdf_page"],
                sections_covered="; ".join(rec["sections"]),
                ocr_ru="\n\n".join(rec["ocr_parts"]),
                translation_uk="\n\n".join(rec["trans_parts"]),
                feynman_notes="\n\n".join(rec["feynman_parts"]),
                misconceptions="",
                figures_json=json.dumps(rec["figures"], ensure_ascii=False),
                status="verified",
            )
            self.save_page(bp)
            seeded_count += 1

        return seeded_count
