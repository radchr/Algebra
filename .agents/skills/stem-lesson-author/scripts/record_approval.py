#!/usr/bin/env python3
"""Record explicit author approval of a brief or scenario."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson_dir", type=Path)
    parser.add_argument("stage", choices=("brief", "scenario"))
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()

    workflow_path = args.lesson_dir / "workflow.json"
    if not workflow_path.is_file():
        print("Missing workflow.json.")
        return 1
    workflow = json.loads(workflow_path.read_text(encoding="utf-8"))
    if args.stage == "scenario" and not (
        workflow.get("brief_approval") or workflow.get("approval_bypassed_by_user") is True
    ):
        print("Approve the brief before approving the scenario.")
        return 1

    workflow[f"{args.stage}_approval"] = {
        "approved_at": datetime.now(UTC).isoformat(),
        "evidence": args.evidence,
    }
    workflow["stage"] = "brief_approved" if args.stage == "brief" else "scenario_approved"
    workflow_path.write_text(
        json.dumps(workflow, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Recorded {args.stage} approval in {workflow_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
