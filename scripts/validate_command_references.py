#!/usr/bin/env python3
"""Validate `/crew ...` references across docs and runtime assets."""

from __future__ import annotations

import re
import sys
from pathlib import Path


COMMAND_PATTERN = re.compile(r"/crew\s+([a-z][a-z-]*)")


def collect_valid_commands(commands_dir: Path) -> set[str]:
    return {path.stem for path in commands_dir.glob("*.md")}


def collect_scan_files(repo_root: Path) -> list[Path]:
    files: set[Path] = set()

    for path in repo_root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        files.add(path)

    additional_assets = [
        repo_root / "install.sh",
        repo_root / "toolkit" / "registry.json",
    ]
    for path in additional_assets:
        if path.exists():
            files.add(path)

    return sorted(files)


def find_invalid_references(
    repo_root: Path, files: list[Path], valid_commands: set[str]
) -> list[tuple[str, int, str, str]]:
    invalid: list[tuple[str, int, str, str]] = []

    for file_path in files:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        for line_number, line in enumerate(lines, start=1):
            for command_name in COMMAND_PATTERN.findall(line):
                if command_name not in valid_commands:
                    invalid.append(
                        (
                            str(file_path.relative_to(repo_root)),
                            line_number,
                            command_name,
                            line.strip(),
                        )
                    )

    return invalid


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    commands_dir = repo_root / "templates" / "shared" / "commands" / "crew"

    if not commands_dir.exists():
        print(f"error: command directory not found: {commands_dir}")
        return 1

    valid_commands = collect_valid_commands(commands_dir)
    scan_files = collect_scan_files(repo_root)
    invalid_references = find_invalid_references(repo_root, scan_files, valid_commands)

    if invalid_references:
        print("Invalid command references found:")
        for rel_path, line_number, command_name, source_line in invalid_references:
            print(f"- {rel_path}:{line_number}: /crew {command_name}")
            print(f"  {source_line}")
        valid_list = ", ".join(sorted(valid_commands))
        print(f"\nValid commands: {valid_list}")
        return 1

    print("Command reference validation passed.")
    print(f"Validated files: {len(scan_files)}")
    print(f"Valid commands: {', '.join(sorted(valid_commands))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
