#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pyyaml==6.0.3",
# ]
# ///
"""Validate that every playbook under playbooks/ is well-formed YAML."""

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
PLAYBOOKS_DIR = REPO_ROOT / "playbooks"


def main() -> int:
    playbook_files = sorted(PLAYBOOKS_DIR.glob("*.yml"))

    if not playbook_files:
        print(f"No playbooks found in {PLAYBOOKS_DIR}")
        return 0

    failures = []
    for path in playbook_files:
        try:
            yaml.safe_load(path.read_text())
            print(f"OK    {path.relative_to(REPO_ROOT)}")
        except yaml.YAMLError as exc:
            failures.append((path, exc))
            print(f"FAIL  {path.relative_to(REPO_ROOT)}: {exc}")

    if failures:
        print(f"\n{len(failures)} playbook(s) failed YAML validation.")
        return 1

    print(f"\nAll {len(playbook_files)} playbook(s) are valid YAML.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
