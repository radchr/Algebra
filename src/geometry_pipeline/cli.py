"""Command-line entry point for geometry content validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .latex_renderer import render_to_files
from .manifest import build_manifest, write_manifest
from .schema import ContentBlock
from .validation import validate_block


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Kiselev geometry content pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate-block", help="Validate one content block")
    validate.add_argument("block", type=Path)
    validate.add_argument(
        "--glossary",
        type=Path,
        default=Path("src/geometry_pipeline/glossary_geometry.json"),
    )
    validate.add_argument("--project-root", type=Path, default=Path.cwd())

    validate_all = subparsers.add_parser(
        "validate-content", help="Validate every JSON block below a content root"
    )
    validate_all.add_argument(
        "--content-root",
        type=Path,
        default=Path("book_geometry/content"),
    )
    validate_all.add_argument(
        "--glossary",
        type=Path,
        default=Path("src/geometry_pipeline/glossary_geometry.json"),
    )
    validate_all.add_argument("--project-root", type=Path, default=Path.cwd())

    manifest = subparsers.add_parser("build-manifest", help="Build a JSONL content manifest")
    manifest.add_argument(
        "--content-root",
        type=Path,
        default=Path("book_geometry/content"),
    )
    manifest.add_argument(
        "--output",
        type=Path,
        default=Path("data/geometry/source_manifest.jsonl"),
    )
    manifest.add_argument("--project-root", type=Path, default=Path.cwd())

    render = subparsers.add_parser(
        "render-latex", help="Render validated content blocks to a review LaTeX document"
    )
    render.add_argument(
        "--content-root",
        type=Path,
        default=Path("book_geometry/content/sections"),
    )
    render.add_argument(
        "--fragment",
        type=Path,
        default=Path("book_geometry/generated/sections/section_01_angles_content.tex"),
    )
    render.add_argument(
        "--review-document",
        type=Path,
        default=Path("book_geometry/review_generated.tex"),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = _parser().parse_args(argv)

    if args.command == "validate-block":
        block = ContentBlock.model_validate_json(args.block.read_text(encoding="utf-8"))
        report = validate_block(
            block,
            project_root=args.project_root.resolve(),
            glossary_path=args.glossary.resolve(),
        )
        print(json.dumps(report.model_dump(mode="json"), ensure_ascii=False, indent=2))
        return 0 if report.passed else 1

    if args.command == "validate-content":
        reports = []
        for path in sorted(args.content_root.resolve().rglob("*.json")):
            block = ContentBlock.model_validate_json(path.read_text(encoding="utf-8"))
            report = validate_block(
                block,
                project_root=args.project_root.resolve(),
                glossary_path=args.glossary.resolve(),
            )
            if report.issues:
                reports.append(report)

        error_count = sum(
            1 for report in reports for issue in report.issues if issue.severity.value == "error"
        )
        warning_count = sum(
            1 for report in reports for issue in report.issues if issue.severity.value == "warning"
        )
        result = {
            "blocks": len(list(args.content_root.resolve().rglob("*.json"))),
            "errors": error_count,
            "warnings": warning_count,
            "reports": [report.model_dump(mode="json") for report in reports],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if error_count else 0

    if args.command == "build-manifest":
        entries = build_manifest(args.content_root.resolve(), args.project_root.resolve())
        write_manifest(entries, args.output.resolve())
        print(f"Wrote {len(entries)} entries to {args.output}")
        return 0

    count = render_to_files(
        args.content_root.resolve(),
        args.fragment.resolve(),
        args.review_document.resolve(),
    )
    print(f"Rendered {count} blocks to {args.fragment}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
