#!/usr/bin/env python3
"""Validate local markdown links to prevent broken references."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:")


def iter_markdown_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in repo_root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        files.append(path)
    return sorted(files)


def normalize_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    return unquote(target)


def should_skip_target(target: str) -> bool:
    if not target:
        return True
    if target.startswith("#"):
        return True
    if target.startswith(SKIP_PREFIXES):
        return True
    return False


def resolve_target(file_path: Path, target: str, repo_root: Path) -> Path:
    path_part = target.split("#", maxsplit=1)[0].strip()
    if path_part.startswith("/"):
        return repo_root / path_part.lstrip("/")
    return (file_path.parent / path_part).resolve()


def find_broken_links(repo_root: Path) -> tuple[list[tuple[str, int, str]], int]:
    broken: list[tuple[str, int, str]] = []
    checked_count = 0

    for file_path in iter_markdown_files(repo_root):
        for line_number, line in enumerate(
            file_path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            for raw_target in LINK_PATTERN.findall(line):
                target = normalize_target(raw_target)
                if should_skip_target(target):
                    continue

                checked_count += 1
                resolved = resolve_target(file_path, target, repo_root)
                if not resolved.exists():
                    broken.append(
                        (
                            str(file_path.relative_to(repo_root)),
                            line_number,
                            target,
                        )
                    )

    return broken, checked_count


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    broken_links, checked_count = find_broken_links(repo_root)

    if broken_links:
        print("Markdown link validation failed:")
        for rel_path, line_number, target in broken_links:
            print(f"- {rel_path}:{line_number}: {target}")
        return 1

    print("Markdown link validation passed.")
    print(f"Validated markdown files: {len(iter_markdown_files(repo_root))}")
    print(f"Validated local links: {checked_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
