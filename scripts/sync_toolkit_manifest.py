#!/usr/bin/env python3
"""Render generated toolkit assets from `toolkit/manifest.json`."""

from __future__ import annotations

import sys
from pathlib import Path

from toolkit_manifest_utils import (
    INSTALL_SCRIPT_FILE,
    MANIFEST_FILE,
    README_FILE,
    RUNTIME_REGISTRY_FILE,
    apply_generated_install_block,
    apply_generated_readme_blocks,
    build_runtime_registry,
    dump_json,
    load_manifest,
    manifest_counts,
    validate_manifest_structure,
    validate_template_references,
)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    manifest = load_manifest(repo_root)

    errors: list[str] = []
    errors.extend(validate_manifest_structure(manifest))
    errors.extend(validate_template_references(repo_root, manifest))

    if errors:
        print("Manifest sync failed due to validation errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    registry_path = repo_root / RUNTIME_REGISTRY_FILE
    registry_path.write_text(
        dump_json(build_runtime_registry(manifest)),
        encoding="utf-8",
    )

    install_path = repo_root / INSTALL_SCRIPT_FILE
    install_text = install_path.read_text(encoding="utf-8")
    install_path.write_text(
        apply_generated_install_block(install_text, manifest),
        encoding="utf-8",
    )

    readme_path = repo_root / README_FILE
    readme_text = readme_path.read_text(encoding="utf-8")
    readme_path.write_text(
        apply_generated_readme_blocks(readme_text, manifest),
        encoding="utf-8",
    )

    counts = manifest_counts(manifest)
    print(f"Synced from {MANIFEST_FILE}:")
    print(f"- Runtime registry: {RUNTIME_REGISTRY_FILE}")
    print(f"- Installer package lists: {INSTALL_SCRIPT_FILE}")
    print(f"- README generated blocks: {README_FILE}")
    print(
        "- Counts: "
        f"skills={counts['skills']}, "
        f"agents={counts['agents']}, "
        f"commands={counts['commands']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
