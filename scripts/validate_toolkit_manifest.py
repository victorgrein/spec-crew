#!/usr/bin/env python3
"""Validate toolkit manifest integrity and generated artifact sync."""

from __future__ import annotations

import sys
from pathlib import Path

from toolkit_manifest_utils import (
    MANIFEST_FILE,
    load_manifest,
    manifest_counts,
    validate_generated_artifacts,
    validate_manifest_structure,
    validate_template_references,
)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = load_manifest(repo_root)

    errors: list[str] = []
    errors.extend(validate_manifest_structure(manifest))
    errors.extend(validate_template_references(repo_root, manifest))
    errors.extend(validate_generated_artifacts(repo_root, manifest))

    if errors:
        print("Toolkit manifest validation failed:")
        for error in errors:
            print(f"- {error}")
        print(
            "Hint: run `python3 scripts/sync_toolkit_manifest.py` after manifest edits."
        )
        return 1

    counts = manifest_counts(manifest)
    print("Toolkit manifest validation passed.")
    print(
        "Validated assets: "
        f"skills={counts['skills']}, "
        f"agents={counts['agents']}, "
        f"commands={counts['commands']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
