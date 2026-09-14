#!/usr/bin/env python3
"""Idempotently deep-merge a JSON patch into a JSON settings file.

Usage: merge_settings.py <target.json> <patch.json>

Merge rules:
  - dict + dict   -> recurse
  - list + list   -> append only patch items not already present (dedup by equality)
  - scalar        -> set only if the key is absent; existing scalars are never
                     overwritten (a note is printed to stderr instead)

Backs up the target file (if it exists) to <target-dir>/backups/<name>.<timestamp>.bak
before writing. Prints CHANGED or OK on the last line depending on whether the
target file content was modified.
"""
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def deep_merge(base, patch, path=""):
    changed = False
    for key, patch_value in patch.items():
        key_path = f"{path}.{key}" if path else key
        if key not in base:
            base[key] = patch_value
            changed = True
        elif isinstance(base[key], dict) and isinstance(patch_value, dict):
            if deep_merge(base[key], patch_value, key_path):
                changed = True
        elif isinstance(base[key], list) and isinstance(patch_value, list):
            for item in patch_value:
                if item not in base[key]:
                    base[key].append(item)
                    changed = True
        elif base[key] != patch_value:
            print(
                f"Note: skipping '{key_path}' - existing value differs from patch, not overwriting",
                file=sys.stderr,
            )
    return changed


def backup(target: Path) -> None:
    backups_dir = target.parent / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = backups_dir / f"{target.name}.{timestamp}.bak"
    shutil.copy2(target, backup_path)


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: merge_settings.py <target.json> <patch.json>", file=sys.stderr)
        sys.exit(1)

    target = Path(sys.argv[1]).expanduser()
    patch_path = Path(sys.argv[2]).expanduser()

    patch = json.loads(patch_path.read_text())

    if target.exists():
        base = json.loads(target.read_text() or "{}")
        backup(target)
    else:
        base = {}
        target.parent.mkdir(parents=True, exist_ok=True)

    changed = deep_merge(base, patch)

    if changed or not target.exists():
        target.write_text(json.dumps(base, indent=2) + "\n")
        print("CHANGED")
    else:
        print("OK")


if __name__ == "__main__":
    main()
