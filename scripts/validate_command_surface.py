#!/usr/bin/env python3
"""Validate canonical command surface and smoke scenarios."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


EXPECTED_CANONICAL_COMMANDS = {"init", "inspect", "fix", "evolve", "docs"}
VALID_OWNERS = {"builder", "auditor", "flow", "docs"}
REQUIRED_CONTRACT_TOKENS = [
    "1. `findings`",
    "2. `plan`",
    "3. `proposed changes`",
    "4. `validation steps`",
]
INVOCATION_PATTERN = re.compile(r"^/crew\s+([a-z][a-z-]*)\b")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(file_path: Path) -> tuple[dict[str, str], str]:
    text = file_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text

    parts = text.split("---", maxsplit=2)
    if len(parts) < 3:
        return {}, text

    _, frontmatter_text, body = parts
    data: dict[str, str] = {}
    for raw_line in frontmatter_text.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", maxsplit=1)
        data[key.strip()] = value.strip().strip('"')

    return data, body


def parse_invocation_command(invocation: str) -> str | None:
    match = INVOCATION_PATTERN.search(invocation.strip())
    if not match:
        return None
    return match.group(1)


def validate_registry_shape(registry: dict) -> list[str]:
    errors: list[str] = []

    commands_data = registry.get("commands")
    if not isinstance(commands_data, dict):
        return ["registry missing `commands` block"]

    canonical_data = commands_data.get("canonical")
    if not isinstance(canonical_data, dict):
        errors.append("registry missing `commands.canonical` block")
        canonical_data = {}

    canonical_commands = set(canonical_data.keys())
    if canonical_commands != EXPECTED_CANONICAL_COMMANDS:
        errors.append(
            "canonical command set mismatch: "
            f"expected {sorted(EXPECTED_CANONICAL_COMMANDS)}, got {sorted(canonical_commands)}"
        )

    for command_name, config in canonical_data.items():
        owner = config.get("owner")
        if owner not in VALID_OWNERS:
            errors.append(
                f"canonical command `{command_name}` has unknown owner `{owner}`"
            )

    return errors


def validate_command_templates(repo_root: Path, registry: dict) -> list[str]:
    errors: list[str] = []

    commands_dir = repo_root / "templates" / "shared" / "commands" / "crew"
    if not commands_dir.exists():
        return [
            f"command template directory missing: {commands_dir.relative_to(repo_root)}"
        ]

    canonical_data = registry["commands"]["canonical"]

    expected_templates = set(canonical_data.keys())
    existing_templates = {path.stem for path in commands_dir.glob("*.md")}

    missing_templates = sorted(expected_templates - existing_templates)
    unexpected_templates = sorted(existing_templates - expected_templates)

    if missing_templates:
        errors.append("missing command templates: " + ", ".join(missing_templates))
    if unexpected_templates:
        errors.append(
            "unexpected command templates: " + ", ".join(unexpected_templates)
        )

    for command_name in canonical_data:
        command_path = commands_dir / f"{command_name}.md"
        if not command_path.exists():
            continue

        frontmatter, body = parse_frontmatter(command_path)

        if frontmatter.get("canonical", "").lower() != "true":
            errors.append(
                f"{command_path.relative_to(repo_root)} missing `canonical: true`"
            )
        expected_command_id = f"crew.{command_name}.v1"
        if frontmatter.get("command_id") != expected_command_id:
            errors.append(
                f"{command_path.relative_to(repo_root)} command_id mismatch: "
                f"expected `{expected_command_id}`, got `{frontmatter.get('command_id', '')}`"
            )

        if f"# /crew {command_name}" not in body:
            errors.append(
                f"{command_path.relative_to(repo_root)} missing canonical heading `# /crew {command_name}`"
            )
        if "## Syntax" not in body:
            errors.append(
                f"{command_path.relative_to(repo_root)} missing `## Syntax` section"
            )
        if "## Response Contract (Required)" not in body:
            errors.append(
                f"{command_path.relative_to(repo_root)} missing `## Response Contract (Required)` section"
            )

        for token in REQUIRED_CONTRACT_TOKENS:
            if token not in body:
                errors.append(
                    f"{command_path.relative_to(repo_root)} missing response contract token `{token}`"
                )

    return errors


def validate_smoke_cases(
    repo_root: Path, registry: dict, smoke_cases: dict
) -> list[str]:
    errors: list[str] = []

    canonical_data = registry["commands"]["canonical"]
    canonical_commands = set(canonical_data.keys())

    canonical_cases = smoke_cases.get("canonical_cases")
    if not isinstance(canonical_cases, list) or not canonical_cases:
        errors.append("smoke case file missing non-empty `canonical_cases` list")
        canonical_cases = []

    seen_ids: set[str] = set()
    covered_canonical: set[str] = set()

    for case in canonical_cases:
        if not isinstance(case, dict):
            errors.append(f"invalid canonical smoke case entry: {case!r}")
            continue

        case_id = case.get("id")
        if not case_id:
            errors.append("canonical smoke case missing `id`")
            continue

        if case_id in seen_ids:
            errors.append(f"duplicate smoke case id: {case_id}")
            continue
        seen_ids.add(case_id)

        invocation = case.get("invocation", "")
        command_name = parse_invocation_command(invocation)
        if not command_name:
            errors.append(
                f"smoke case `{case_id}` has invalid invocation: {invocation!r}"
            )
            continue

        if command_name not in canonical_commands:
            errors.append(
                f"canonical smoke case `{case_id}` must invoke canonical command, got `{command_name}`"
            )
            continue

        covered_canonical.add(command_name)

        expected_command = case.get("expected_command")
        if expected_command and command_name != expected_command:
            errors.append(
                f"smoke case `{case_id}` invokes `{command_name}`, expected `{expected_command}`"
            )

        expected_owner = case.get("expected_owner")
        if expected_owner:
            owner = canonical_data.get(command_name, {}).get("owner")
            if owner != expected_owner:
                errors.append(
                    f"smoke case `{case_id}` owner mismatch: expected `{expected_owner}`, got `{owner}`"
                )

        template_path = (
            repo_root
            / "templates"
            / "shared"
            / "commands"
            / "crew"
            / f"{command_name}.md"
        )
        if not template_path.exists():
            errors.append(
                f"smoke case `{case_id}` maps to missing template `{template_path.relative_to(repo_root)}`"
            )

    missing_canonical = sorted(canonical_commands - covered_canonical)
    if missing_canonical:
        errors.append(
            "canonical commands not covered by smoke cases: "
            + ", ".join(missing_canonical)
        )

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    registry_path = repo_root / "toolkit" / "registry.json"
    smoke_cases_path = repo_root / "toolkit" / "cases" / "command-smoke.json"

    if not registry_path.exists():
        print(f"error: registry not found: {registry_path}")
        return 1
    if not smoke_cases_path.exists():
        print(f"error: smoke cases not found: {smoke_cases_path}")
        return 1

    registry = load_json(registry_path)
    smoke_cases = load_json(smoke_cases_path)

    errors: list[str] = []
    errors.extend(validate_registry_shape(registry))
    if not errors:
        errors.extend(validate_command_templates(repo_root, registry))
        errors.extend(validate_smoke_cases(repo_root, registry, smoke_cases))

    if errors:
        print("Command surface validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    canonical_count = len(registry["commands"]["canonical"])
    smoke_count = len(smoke_cases["canonical_cases"])

    print("Command surface validation passed.")
    print(f"Validated canonical commands: {canonical_count}")
    print(f"Validated smoke cases: {smoke_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
