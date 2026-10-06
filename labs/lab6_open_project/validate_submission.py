"""Mechanical Lab 6 submission checker.

This intentionally checks presence/metadata only. It cannot validate scientific
quality, novelty, or whether a representation is well justified.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys

REQUIRED_DOCS = [
    "PROJECT_BRIEF.md", "PRIOR_ART_AND_CLAIM.md", "REPRESENTATION_CARD.md",
    "EXPERIMENT_PLAN.md", "FINAL_REPORT.md", "reproducibility.json",
]
REQUIRED_META = ["capture", "code_revision", "environment", "split", "random_seeds",
                 "preprocessing", "raw_observable_budget", "representation_budget"]

def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for name in REQUIRED_DOCS:
        if not (root / name).is_file():
            errors.append(f"missing required file: {name}")
    meta_path = root / "reproducibility.json"
    if meta_path.is_file():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid reproducibility.json: {exc}")
        else:
            for key in REQUIRED_META:
                if key not in meta:
                    errors.append(f"missing reproducibility key: {key}")
    for dirname in ["src", "results"]:
        if not (root / dirname).is_dir():
            errors.append(f"missing required directory: {dirname}/")
    return errors

def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("lab6_submission")
    errors = validate(root)
    if errors:
        print("Lab 6 submission check: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Lab 6 submission check: PASS (mechanical checks only)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
