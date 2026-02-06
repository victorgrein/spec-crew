#!/usr/bin/env python3
"""Validate phase-4 skill trigger coverage and deterministic command mapping."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter_lists(path: Path) -> dict[str, list[str] | str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}

    _, frontmatter_text, _ = text.split("---", maxsplit=2)
    lines = frontmatter_text.splitlines()
    data: dict[str, list[str] | str] = {}

    index = 0
    while index < len(lines):
        raw = lines[index]
        line = raw.strip()
        if not line:
            index += 1
            continue
        if ":" not in line:
            index += 1
            continue

        key, value = line.split(":", maxsplit=1)
        key = key.strip()
        value = value.strip().strip('"')

        if value:
            data[key] = value
            index += 1
            continue

        values: list[str] = []
        cursor = index + 1
        while cursor < len(lines):
            item = lines[cursor].strip()
            if item.startswith("- "):
                values.append(item[2:].strip().strip('"'))
                cursor += 1
                continue
            break

        data[key] = values
        index = cursor

    return data


def validate_trigger_uniqueness(skill_registry: dict) -> list[str]:
    errors: list[str] = []
    seen: dict[str, str] = {}

    for skill_name, config in skill_registry["canonical"].items():
        triggers = config.get("triggers", [])
        if not triggers:
            errors.append(f"canonical skill `{skill_name}` has no triggers")
            continue

        for trigger in triggers:
            normalized = " ".join(trigger.lower().split())
            if normalized in seen:
                errors.append(
                    f"duplicate trigger `{trigger}` shared by `{skill_name}` and `{seen[normalized]}`"
                )
            else:
                seen[normalized] = skill_name

    return errors


def validate_command_policy(registry: dict) -> list[str]:
    errors: list[str] = []

    canonical_commands = set(registry["commands"]["canonical"].keys())
    canonical_skills = set(registry["skills"]["canonical"].keys())
    command_policy = registry["skills"]["command_policy"]

    if set(command_policy.keys()) != canonical_commands:
        errors.append(
            "command policy mismatch with canonical command set: "
            f"policy={sorted(command_policy.keys())}, commands={sorted(canonical_commands)}"
        )

    for command_name, policy in command_policy.items():
        primary = policy.get("primary")
        optional = policy.get("optional", [])

        if primary not in canonical_skills:
            errors.append(
                f"command `{command_name}` primary skill `{primary}` is not canonical"
            )

        if not isinstance(optional, list):
            errors.append(f"command `{command_name}` optional skills must be a list")
            continue

        if len(optional) != len(set(optional)):
            errors.append(f"command `{command_name}` optional skills contain duplicates")

        for skill_name in optional:
            if skill_name not in canonical_skills:
                errors.append(
                    f"command `{command_name}` optional skill `{skill_name}` is not canonical"
                )
            if skill_name == primary:
                errors.append(
                    f"command `{command_name}` optional skills include primary skill `{primary}`"
                )

    covered = {
        policy["primary"]
        for policy in command_policy.values()
        if isinstance(policy, dict) and "primary" in policy
    }
    for policy in command_policy.values():
        if isinstance(policy, dict):
            covered.update(policy.get("optional", []))

    uncovered = sorted(canonical_skills - covered)
    if uncovered:
        errors.append("canonical skills not used by any command policy: " + ", ".join(uncovered))

    return errors


def validate_agent_alignment(repo_root: Path, registry: dict) -> list[str]:
    errors: list[str] = []

    agents_dir = repo_root / "templates" / "shared" / "agents" / "crewai"
    command_owners = {
        command: data["owner"] for command, data in registry["commands"]["canonical"].items()
    }
    command_policy = registry["skills"]["command_policy"]
    canonical_agents = set(registry["agents"]["canonical"].keys())
    canonical_skills = set(registry["skills"]["canonical"].keys())

    agent_skill_map: dict[str, set[str]] = {}
    for agent_name in canonical_agents:
        agent_file = agents_dir / f"{agent_name}.md"
        if not agent_file.exists():
            errors.append(f"missing canonical agent file: {agent_file.relative_to(repo_root)}")
            continue

        metadata = parse_frontmatter_lists(agent_file)
        skills = metadata.get("skills", [])
        if not isinstance(skills, list):
            errors.append(f"agent `{agent_name}` has invalid skills frontmatter")
            continue

        unknown = sorted(set(skills) - canonical_skills)
        if unknown:
            errors.append(
                f"agent `{agent_name}` uses non-canonical skills: {', '.join(unknown)}"
            )

        agent_skill_map[agent_name] = set(skills)

    for command_name, policy in command_policy.items():
        owner = command_owners.get(command_name)
        owner_skills = agent_skill_map.get(owner or "", set())
        primary = policy.get("primary")
        optional = policy.get("optional", [])

        if primary and primary not in owner_skills:
            errors.append(
                f"command `{command_name}` owner `{owner}` missing primary skill `{primary}`"
            )

        for skill_name in optional:
            if skill_name not in owner_skills:
                errors.append(
                    f"command `{command_name}` owner `{owner}` missing optional skill `{skill_name}`"
                )

    for skill_name, config in registry["skills"]["canonical"].items():
        owners = config.get("owners", [])
        for owner in owners:
            if owner not in canonical_agents:
                errors.append(
                    f"canonical skill `{skill_name}` references unknown owner `{owner}`"
                )

    return errors


def validate_orchestrator_mentions(repo_root: Path, registry: dict) -> list[str]:
    errors: list[str] = []
    canonical_skills = sorted(registry["skills"]["canonical"].keys())

    orchestrator_files = [
        repo_root / "templates" / "claude" / "CLAUDE.md",
        repo_root / "templates" / "opencode" / "crewai-orchestrator.md",
    ]

    for file_path in orchestrator_files:
        text = file_path.read_text(encoding="utf-8")
        for skill_name in canonical_skills:
            if skill_name not in text:
                errors.append(
                    f"orchestrator file missing canonical skill `{skill_name}`: {file_path.relative_to(repo_root)}"
                )

    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    registry_path = repo_root / "toolkit" / "registry.json"

    if not registry_path.exists():
        print(f"error: registry not found: {registry_path}")
        return 1

    registry = load_json(registry_path)
    errors: list[str] = []

    errors.extend(validate_trigger_uniqueness(registry["skills"]))
    errors.extend(validate_command_policy(registry))
    errors.extend(validate_agent_alignment(repo_root, registry))
    errors.extend(validate_orchestrator_mentions(repo_root, registry))

    if errors:
        print("Skill routing validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    command_count = len(registry["skills"]["command_policy"])
    trigger_count = sum(
        len(config.get("triggers", []))
        for config in registry["skills"]["canonical"].values()
    )
    print("Skill routing validation passed.")
    print(f"Validated command policies: {command_count}")
    print(f"Validated canonical trigger phrases: {trigger_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
