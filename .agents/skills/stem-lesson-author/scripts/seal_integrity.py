#!/usr/bin/env python3
"""Seal the original prompt and locked brief blocks for later verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

LOCKED_BLOCK = re.compile(r"\[ЗБЕРЕГТИ ДОСЛІВНО\](.*?)\[/ЗБЕРЕГТИ ДОСЛІВНО\]", re.DOTALL)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson_dir", type=Path)
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="replace an existing seal only after explicit author permission",
    )
    args = parser.parse_args()

    source_path = args.lesson_dir / "source_prompt.md"
    brief_path = args.lesson_dir / "lesson_brief.md"
    integrity_path = args.lesson_dir / "integrity.json"
    if not source_path.is_file() or not brief_path.is_file():
        print("Missing source_prompt.md or lesson_brief.md.")
        return 1

    source = source_path.read_text(encoding="utf-8")
    brief = brief_path.read_text(encoding="utf-8")
    if not source:
        print("source_prompt.md is empty; copy the author's input exactly first.")
        return 1
    if source not in brief:
        print("The exact source prompt is not present in lesson_brief.md.")
        return 1

    if integrity_path.is_file() and not args.refresh:
        current = json.loads(integrity_path.read_text(encoding="utf-8"))
        if current.get("source_prompt_sha256"):
            print("Integrity seal already exists; refusing to replace it.")
            return 1

    locked = LOCKED_BLOCK.findall(brief)
    payload = {
        "version": 1,
        "source_prompt_sha256": sha256_text(source),
        "locked_blocks_sha256": [sha256_text(block) for block in locked],
    }
    integrity_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Integrity seal written: {integrity_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
