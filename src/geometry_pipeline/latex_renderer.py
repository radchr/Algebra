"""Deterministic LaTeX rendering for validated geometry content blocks."""

from __future__ import annotations

import re
from pathlib import Path

from .schema import AdaptationKind, ContentBlock

MATH_PATTERN = re.compile(r"(\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$))", re.DOTALL)
LINK_PATTERN = re.compile(r"\[([^]]+)]\((https?://[^)]+)\)")
INLINE_STYLE_PATTERN = re.compile(r"(\*\*.*?\*\*|(?<!\*)\*(?!\*).*?(?<!\*)\*(?!\*))")
NUMBERED_ITEM_PATTERN = re.compile(r"^\s*\d+\.\s+(.*)$")
BULLET_ITEM_PATTERN = re.compile(r"^\s*[-*]\s+(.*)$")


def _escape_plain(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def _render_styled_plain(text: str) -> str:
    output: list[str] = []
    cursor = 0
    for match in INLINE_STYLE_PATTERN.finditer(text):
        output.append(_escape_plain(text[cursor : match.start()]))
        token = match.group(0)
        if token.startswith("**"):
            output.append(r"\textbf{" + _escape_plain(token[2:-2]) + "}")
        else:
            output.append(r"\emph{" + _escape_plain(token[1:-1]) + "}")
        cursor = match.end()
    output.append(_escape_plain(text[cursor:]))
    return "".join(output)


def _render_inline(text: str) -> str:
    """Render a deliberately small Markdown subset while preserving TeX math."""

    protected: list[str] = []

    def protect_math(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.startswith("$$"):
            token = "\\[\n" + token[2:-2].strip() + "\n\\]"
        else:
            token = token.replace(", ", r",\allowbreak ")
        protected.append(token)
        return f"GEOMTOKEN{len(protected) - 1}END"

    def protect_link(match: re.Match[str]) -> str:
        label = _escape_plain(match.group(1))
        protected.append(r"\href{" + match.group(2) + "}{" + label + "}")
        return f"GEOMTOKEN{len(protected) - 1}END"

    value = MATH_PATTERN.sub(protect_math, text)
    value = LINK_PATTERN.sub(protect_link, value)
    value = _render_styled_plain(value)
    for index, token in enumerate(protected):
        value = value.replace(f"GEOMTOKEN{index}END", token)
    return value


def markdown_to_latex(text: str) -> str:
    """Convert the content schema's constrained Markdown dialect to LaTeX."""

    output: list[str] = []
    active_list: str | None = None

    def close_list() -> None:
        nonlocal active_list
        if active_list:
            output.append(rf"\end{{{active_list}}}")
            active_list = None

    lines = text.splitlines()
    for line_index, raw_line in enumerate(lines):
        line = raw_line.rstrip()
        if not line.strip():
            next_line = next(
                (candidate for candidate in lines[line_index + 1 :] if candidate.strip()), ""
            )
            continues_numbered = active_list == "enumerate" and NUMBERED_ITEM_PATTERN.match(
                next_line
            )
            continues_bullet = active_list == "itemize" and BULLET_ITEM_PATTERN.match(next_line)
            if not continues_numbered and not continues_bullet:
                close_list()
                output.append("")
            continue

        numbered = NUMBERED_ITEM_PATTERN.match(line)
        bullet = BULLET_ITEM_PATTERN.match(line)
        requested_list = "enumerate" if numbered else "itemize" if bullet else None
        if requested_list:
            if active_list != requested_list:
                close_list()
                output.append(rf"\begin{{{requested_list}}}")
                active_list = requested_list
            item_text = numbered.group(1) if numbered else bullet.group(1)
            output.append(r"\item " + _render_inline(item_text))
            continue

        close_list()
        output.append(_render_inline(line))

    close_list()
    return "\n".join(output).strip()


def _source_comment(block: ContentBlock) -> str:
    pages = ", ".join(str(source.printed_page) for source in block.sources)
    return f"% block: {block.id}; printed source pages: {pages}"


def _render_figures(block: ContentBlock) -> str:
    if not block.figures:
        return ""
    lines = [r"\begin{center}"]
    rendered_sources: set[str] = set()
    for figure in block.figures:
        number = figure.source_number or figure.id
        if figure.vector_source and figure.vector_source not in rendered_sources:
            latex_path = figure.vector_source.removeprefix("book_geometry/")
            lines.append(rf"\input{{{latex_path}}}")
            rendered_sources.add(figure.vector_source)
        else:
            if not figure.vector_source:
                lines.extend(
                    [
                        r"\fbox{\parbox{0.82\textwidth}{\centering\small",
                        rf"Місце для реконструкції рисунка {number}.\\",
                        rf"\texttt{{{_escape_plain(figure.id)}}}",
                        r"}}\\[6pt]",
                    ]
                )
        caption = f"Рис. {number}."
        if figure.alt_uk:
            caption += f" {figure.alt_uk}"
        lines.append(rf"{{\small\textbf{{{_escape_plain(caption)}}}}}\\[6pt]")
    lines.append(r"\end{center}")
    return "\n".join(lines)


def _render_adaptation(block: ContentBlock, index: int) -> str:
    adaptation = block.adaptations[index]
    body = markdown_to_latex(adaptation.text_uk)
    if adaptation.kind is AdaptationKind.INTERACTIVE_LINK:
        if adaptation.qr_asset:
            url = adaptation.citations[0]
            title = markdown_to_latex(adaptation.title_uk or "Інтерактивний матеріал")
            return "\n".join(
                [
                    rf"\motionlink{{{title}}}%",
                    rf"{{{body}}}%",
                    rf"{{{url}}}%",
                    rf"{{{adaptation.qr_asset}}}",
                ]
            )
        environment = "mediabox"
        default_title = "Інтерактивний матеріал"
    elif adaptation.kind is AdaptationKind.WORKED_SOLUTION:
        environment = "scaffoldbox"
        default_title = "Розв'язання або доведення"
    elif adaptation.kind is AdaptationKind.PROOF_GUIDE:
        environment = "scaffoldbox"
        default_title = "Дороговказ доведення"
    elif adaptation.kind is AdaptationKind.MISCONCEPTION:
        environment = "warningbox"
        default_title = "Пастка мислення"
    else:
        environment = "feynmanbox"
        default_title = "Редакторське пояснення"
    title = markdown_to_latex(adaptation.title_uk or default_title)
    return f"\\begin{{{environment}}}[{title}]\n{body}\n\\end{{{environment}}}"


def render_block(block: ContentBlock) -> str:
    """Render one validated block without consulting global context."""

    if block.translation is None:
        raise ValueError(f"Block {block.id} has no Ukrainian translation")

    parts = [_source_comment(block)]
    if block.kind.value == "exercise":
        parts.extend(
            [
                rf"\begin{{problem}}[{_escape_plain(block.title_uk)}]",
                markdown_to_latex(block.translation.text_uk),
                r"\end{problem}",
            ]
        )
    else:
        title = _escape_plain(block.title_uk.rstrip("."))
        parts.extend(
            [
                rf"\paragraph{{{_escape_plain(block.ordinal)}. {title}.}}",
                markdown_to_latex(block.translation.text_uk),
            ]
        )

    figures = _render_figures(block)
    if figures:
        parts.append(figures)
    parts.extend(_render_adaptation(block, index) for index in range(len(block.adaptations)))
    return "\n\n".join(parts)


def _sort_key(block: ContentBlock) -> tuple[int, int]:
    first_printed_page = min(source.printed_page or source.pdf_page for source in block.sources)
    exercise_offset = 100 if block.kind.value == "exercise" else 0
    return (first_printed_page, exercise_offset + int(block.ordinal))


def load_blocks(content_root: Path) -> list[ContentBlock]:
    blocks = [
        ContentBlock.model_validate_json(path.read_text(encoding="utf-8"))
        for path in sorted(content_root.rglob("*.json"))
    ]
    return sorted(blocks, key=_sort_key)


def _is_introduction(block: ContentBlock) -> bool:
    return any(source.section == "Введение" for source in block.sources)


def render_introduction(blocks: list[ContentBlock]) -> str:
    introduction = [block for block in blocks if _is_introduction(block)]
    parts = [
        "% Generated by geometry_pipeline.latex_renderer. Do not edit by hand.",
        r"\chapter*{Вступні поняття}",
        r"\addcontentsline{toc}{chapter}{Вступні поняття}",
        (
            r"\begin{tcolorbox}[colback=boxbglight,colframe=primaryblue,"
            r"title={ЯК ЧИТАТИ ЦЕЙ ВСТУП},fonttitle=\bfseries\sffamily,breakable]"
        ),
        (
            "Параграфи 1--12 вводять базову мову геометрії. Основний текст є сучасною "
            "українською адаптацією Кисельова; редакторські уточнення виділено окремо."
        ),
        r"\end{tcolorbox}",
    ]
    parts.extend(render_block(block) for block in introduction)
    return "\n\n".join(parts) + "\n"


def render_section(blocks: list[ContentBlock]) -> str:
    sections = [
        block for block in blocks if block.kind.value != "exercise" and not _is_introduction(block)
    ]
    exercises = [block for block in blocks if block.kind.value == "exercise"]
    parts = [
        "% Generated by geometry_pipeline.latex_renderer. Do not edit by hand.",
        r"\chapter{Кути. Суміжні та вертикальні кути}",
        (
            r"\begin{tcolorbox}[colback=boxbglight,colframe=primaryblue,"
            r"coltitle=white,fonttitle=\bfseries\sffamily,title={СТАТУС АВТОМАТИЧНОЇ "
            r"ЗБІРКИ},arc=3mm,boxrule=1.2pt,breakable]"
        ),
        (
            "Цей файл згенеровано зі структурованих блоків. Позначені місця рисунків "
            "очікують векторної реконструкції та редакторського перегляду."
        ),
        r"\end{tcolorbox}",
    ]
    parts.extend(render_block(block) for block in sections)
    if exercises:
        parts.extend([r"\clearpage", r"\section{Вправи}"])
        parts.extend(render_block(block) for block in exercises)
    return "\n\n".join(parts) + "\n"


def write_review_document(fragment_paths: list[Path], review_path: Path) -> None:
    preamble_path = review_path.parent / "preamble.tex"
    if not preamble_path.is_file():
        raise FileNotFoundError(f"Review preamble not found: {preamble_path}")
    preamble = preamble_path.read_text(encoding="utf-8").strip()
    fragments = "\n\n".join(
        fragment_path.read_text(encoding="utf-8").strip() for fragment_path in fragment_paths
    )
    document = "\n".join(
        [
            r"\documentclass[11pt,a4paper,oneside]{book}",
            "% Inlined from preamble.tex for standalone review compilation.",
            preamble,
            r"\begin{document}",
            "% Inlined generated section fragment.",
            fragments,
            r"\end{document}",
            "",
        ]
    )
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(document, encoding="utf-8")


def render_to_files(content_root: Path, fragment_path: Path, review_path: Path) -> int:
    blocks = load_blocks(content_root)
    fragment_path.parent.mkdir(parents=True, exist_ok=True)
    introduction_path = fragment_path.parent / "00_introduction.tex"
    introduction_path.write_text(render_introduction(blocks), encoding="utf-8")
    fragment_path.write_text(render_section(blocks), encoding="utf-8")
    write_review_document([introduction_path, fragment_path], review_path)
    return len(blocks)
