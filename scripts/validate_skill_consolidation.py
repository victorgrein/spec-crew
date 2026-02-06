#!/usr/bin/env python3
"""Validate canonical skill packs and installer coverage."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


EXPECTED_CANONICAL_SKILLS = [
    "core-build",
    "flows",
    "governance",
    "migration",
    "runtime",
    "tools",
]

MAX_CANONICAL_LINES = 70
MAX_TOTAL_LINES = 600


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}

    _, frontmatter_text, _ = text.split("---", maxsplit=2)
    data: dict[str, str] = {}
    for raw_line in frontmatter_text.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", maxsplit=1)
        data[key.strip()] = value.strip().strip('"')
    return data


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def parse_bash_array(script_text: str, array_name: str) -> list[str]:
    pattern = rf"{array_name}=\((.*?)\)"
    match = re.search(pattern, script_text, flags=re.DOTALL)
    if not match:
        return []
    return re.findall(r'"([^\"]+)"', match.group(1))


def validate_canonical_skills(repo_root: Path, registry: dict) -> tuple[list[str], int]:
    errors: list[str] = []
    total_lines = 0

    skills_dir = repo_root / "templates" / "shared" / "skills"
    canonical = registry["skills"]["canonical"]
    canonical_names = sorted(canonical.keys())

    if canonical_names != EXPECTED_CANONICAL_SKILLS:
        errors.append(
            "canonical skill set mismatch: "
            f"expected {EXPECTED_CANONICAL_SKILLS}, got {canonical_names}"
        )

    for skill_name, config in canonical.items():
        skill_path = skills_dir / skill_name / "SKILL.md"
        if not skill_path.exists():
            errors.append(f"missing canonical skill file: {skill_path.relative_to(repo_root)}")
            continue

        fm = parse_frontmatter(skill_path)
        if fm.get("name") != skill_name:
            errors.append(
                f"{skill_path.relative_to(repo_root)} name mismatch: "
                f"expected `{skill_name}`, got `{fm.get('name', '')}`"
            )

        lines = line_count(skill_path)
        total_lines += lines
        if lines > MAX_CANONICAL_LINES:
            errors.append(
                f"canonical skill prompt too large ({lines} lines): {skill_path.relative_to(repo_root)}"
            )

        triggers = config.get("triggers", [])
        if not triggers:
            errors.append(f"canonical skill `{skill_name}` has no triggers")

    existing_skill_dirs = {
        path.name
        for path in skills_dir.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists()
    }
    unexpected = sorted(existing_skill_dirs - set(canonical.keys()))
    if unexpected:
        errors.append(
            "unexpected non-canonical skill packs present: " + ", ".join(unexpected)
        )

    return errors, total_lines


def validate_installer_skills(repo_root: Path, registry: dict) -> list[str]:
    errors: list[str] = []

    install_script = repo_root / "install.sh"
    script_text = install_script.read_text(encoding="utf-8")
    installed_skills = set(parse_bash_array(script_text, "PKG_SKILLS"))

    expected_skills = set(registry["skills"]["canonical"].keys())

    missing = sorted(expected_skills - installed_skills)
    unexpected = sorted(installed_skills - expected_skills)

    if missing:
        errors.append("install.sh missing skill package entries: " + ", ".join(missing))
    if unexpected:
        errors.append("install.sh has unexpected skill package entries: " + ", ".join(unexpected))

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    registry_path = repo_root / "toolkit" / "registry.json"

    if not registry_path.exists():
        print(f"error: registry not found: {registry_path}")
        return 1

    registry = load_json(registry_path)

    errors: list[str] = []
    canonical_lines = 0

    canonical_errors, canonical_lines = validate_canonical_skills(repo_root, registry)
    errors.extend(canonical_errors)
    errors.extend(validate_installer_skills(repo_root, registry))

    total_lines = canonical_lines
    if total_lines > MAX_TOTAL_LINES:
        errors.append(
            f"total skill prompt budget exceeded: {total_lines} > {MAX_TOTAL_LINES} lines"
        )

    if errors:
        print("Skill consolidation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill consolidation validation passed.")
    print(f"Canonical skill packs: {len(registry['skills']['canonical'])}")
    print(f"Canonical prompt lines: {canonical_lines}")
    print(f"Total prompt lines: {total_lines}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
