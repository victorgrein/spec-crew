#!/usr/bin/env python3
"""Shared utilities for toolkit manifest generation and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANIFEST_FILE = "toolkit/manifest.json"
MANIFEST_SCHEMA_FILE = "toolkit/manifest.schema.json"
RUNTIME_REGISTRY_FILE = "toolkit/registry.json"
INSTALL_SCRIPT_FILE = "install.sh"
README_FILE = "README.md"

INSTALL_BLOCK_BEGIN = "# BEGIN GENERATED: TOOLKIT_PACKAGE_LISTS"
INSTALL_BLOCK_END = "# END GENERATED: TOOLKIT_PACKAGE_LISTS"

README_WHATS_INSIDE_BEGIN = "<!-- BEGIN GENERATED: TOOLKIT_WHATS_INSIDE -->"
README_WHATS_INSIDE_END = "<!-- END GENERATED: TOOLKIT_WHATS_INSIDE -->"
README_INSTALLER_COUNTS_BEGIN = "<!-- BEGIN GENERATED: TOOLKIT_INSTALLER_COUNTS -->"
README_INSTALLER_COUNTS_END = "<!-- END GENERATED: TOOLKIT_INSTALLER_COUNTS -->"
README_INDEX_BEGIN = "<!-- BEGIN GENERATED: TOOLKIT_INDEX -->"
README_INDEX_END = "<!-- END GENERATED: TOOLKIT_INDEX -->"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2) + "\n"


def load_manifest(repo_root: Path) -> dict[str, Any]:
    return load_json(repo_root / MANIFEST_FILE)


def keys_in_order(data: dict[str, Any]) -> list[str]:
    return list(data.keys())


def command_canonical_names(manifest: dict[str, Any]) -> list[str]:
    return keys_in_order(manifest["commands"]["canonical"])


def agent_canonical_names(manifest: dict[str, Any]) -> list[str]:
    return keys_in_order(manifest["agents"]["canonical"])


def skill_canonical_names(manifest: dict[str, Any]) -> list[str]:
    return keys_in_order(manifest["skills"]["canonical"])


def workflow_names(manifest: dict[str, Any]) -> list[str]:
    return keys_in_order(manifest["workflows"]["canonical"])


def manifest_counts(manifest: dict[str, Any]) -> dict[str, int]:
    skills = len(skill_canonical_names(manifest))
    agents = len(agent_canonical_names(manifest))
    commands = len(command_canonical_names(manifest))
    workflows = len(workflow_names(manifest))

    return {
        "skills": skills,
        "agents": agents,
        "commands": commands,
        "workflows": workflows,
    }


def build_package_lists(manifest: dict[str, Any]) -> dict[str, list[str]]:
    skill_packages = skill_canonical_names(manifest)
    agent_packages = [f"crewai/{name}" for name in agent_canonical_names(manifest)]
    workflow_packages = workflow_names(manifest)
    command_packages = [f"crew/{name}" for name in command_canonical_names(manifest)]

    return {
        "PKG_SKILLS": skill_packages,
        "PKG_AGENTS": agent_packages,
        "PKG_WORKFLOWS": workflow_packages,
        "PKG_COMMANDS": command_packages,
    }


def build_runtime_registry(manifest: dict[str, Any]) -> dict[str, Any]:
    command_canonical = {
        name: {"owner": config["owner"]}
        for name, config in manifest["commands"]["canonical"].items()
    }

    agent_canonical = {
        name: {"description": config["description"]}
        for name, config in manifest["agents"]["canonical"].items()
    }

    skill_canonical = {
        name: {
            "owners": config["owners"],
            "triggers": config["triggers"],
        }
        for name, config in manifest["skills"]["canonical"].items()
    }

    return {
        "schema_version": manifest["schema_version"],
        "phase": manifest["phase"],
        "commands": {
            "canonical": command_canonical,
        },
        "agents": {
            "canonical": agent_canonical,
        },
        "skills": {
            "canonical": skill_canonical,
            "command_policy": manifest["skills"]["command_policy"],
        },
    }


def render_bash_array(name: str, values: list[str]) -> str:
    lines = [f"{name}=("]
    lines.extend(f'    "{value}"' for value in values)
    lines.append(")")
    return "\n".join(lines)


def render_install_block(manifest: dict[str, Any]) -> str:
    package_lists = build_package_lists(manifest)
    lines = [
        INSTALL_BLOCK_BEGIN,
        render_bash_array("PKG_SKILLS", package_lists["PKG_SKILLS"]),
        "",
        render_bash_array("PKG_AGENTS", package_lists["PKG_AGENTS"]),
        "",
        render_bash_array("PKG_WORKFLOWS", package_lists["PKG_WORKFLOWS"]),
        "",
        render_bash_array("PKG_COMMANDS", package_lists["PKG_COMMANDS"]),
        INSTALL_BLOCK_END,
    ]
    return "\n".join(lines)


def format_code_list(items: list[str], prefix: str = "") -> str:
    return ", ".join(f"`{prefix}{item}`" for item in items)


def render_readme_whats_inside_block(manifest: dict[str, Any]) -> str:
    counts = manifest_counts(manifest)
    lines = [
        README_WHATS_INSIDE_BEGIN,
        f"- **{counts['skills']} Skill Packs**",
        f"- **{counts['agents']} Core Agents**",
        f"- **{counts['commands']} Canonical Commands**",
        f"- **{counts['workflows']} Workflows** that guide you step by step",
        README_WHATS_INSIDE_END,
    ]
    return "\n".join(lines)


def render_readme_installer_counts_block(manifest: dict[str, Any]) -> str:
    counts = manifest_counts(manifest)
    lines = [
        README_INSTALLER_COUNTS_BEGIN,
        f"- {counts['skills']} Skills",
        f"- {counts['agents']} Agents",
        f"- {counts['workflows']} Workflows",
        f"- {counts['commands']} Commands",
        README_INSTALLER_COUNTS_END,
    ]
    return "\n".join(lines)


def render_readme_index_block(manifest: dict[str, Any]) -> str:
    canonical_commands = command_canonical_names(manifest)
    canonical_agents = agent_canonical_names(manifest)
    canonical_skills = skill_canonical_names(manifest)
    workflows = workflow_names(manifest)

    lines = [
        README_INDEX_BEGIN,
        f"- **Canonical commands ({len(canonical_commands)}):** {format_code_list(canonical_commands, '/crew ')}",
        f"- **Canonical agents ({len(canonical_agents)}):** {format_code_list(canonical_agents)}",
        f"- **Canonical skill packs ({len(canonical_skills)}):** {format_code_list(canonical_skills)}",
        f"- **Workflows ({len(workflows)}):** {format_code_list(workflows)}",
        README_INDEX_END,
    ]
    return "\n".join(lines)


def replace_block(text: str, begin_marker: str, end_marker: str, block: str) -> str:
    start = text.find(begin_marker)
    if start == -1:
        raise ValueError(f"missing start marker: {begin_marker}")

    end = text.find(end_marker, start)
    if end == -1:
        raise ValueError(f"missing end marker: {end_marker}")

    replacement = block
    if not replacement.endswith("\n"):
        replacement += "\n"

    return text[:start] + replacement + text[end + len(end_marker) :]


def extract_block(text: str, begin_marker: str, end_marker: str) -> str:
    start = text.find(begin_marker)
    if start == -1:
        raise ValueError(f"missing start marker: {begin_marker}")

    end = text.find(end_marker, start)
    if end == -1:
        raise ValueError(f"missing end marker: {end_marker}")

    end += len(end_marker)
    return text[start:end]


def apply_generated_install_block(install_text: str, manifest: dict[str, Any]) -> str:
    return replace_block(
        install_text,
        INSTALL_BLOCK_BEGIN,
        INSTALL_BLOCK_END,
        render_install_block(manifest),
    )


def apply_generated_readme_blocks(readme_text: str, manifest: dict[str, Any]) -> str:
    updated = replace_block(
        readme_text,
        README_WHATS_INSIDE_BEGIN,
        README_WHATS_INSIDE_END,
        render_readme_whats_inside_block(manifest),
    )
    updated = replace_block(
        updated,
        README_INSTALLER_COUNTS_BEGIN,
        README_INSTALLER_COUNTS_END,
        render_readme_installer_counts_block(manifest),
    )
    updated = replace_block(
        updated,
        README_INDEX_BEGIN,
        README_INDEX_END,
        render_readme_index_block(manifest),
    )
    return updated


def check_string_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def validate_manifest_structure(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    required_top = [
        "schema_version",
        "phase",
        "commands",
        "agents",
        "skills",
        "workflows",
        "installation",
    ]
    for key in required_top:
        if key not in manifest:
            errors.append(f"manifest missing top-level key `{key}`")

    if errors:
        return errors

    if manifest.get("schema_version") != "1.0":
        errors.append(
            f"unsupported schema_version `{manifest.get('schema_version')}`; expected `1.0`"
        )

    commands = manifest["commands"]
    agents = manifest["agents"]
    skills = manifest["skills"]
    workflows = manifest["workflows"]
    installation = manifest["installation"]

    for section_name, section in [
        ("commands", commands),
        ("agents", agents),
        ("workflows", workflows),
    ]:
        if not isinstance(section, dict):
            errors.append(f"manifest `{section_name}` must be an object")
            continue
        if "canonical" not in section or not isinstance(section["canonical"], dict):
            errors.append(f"manifest missing `{section_name}.canonical` object")

    if not isinstance(skills, dict):
        errors.append("manifest `skills` must be an object")
    else:
        if "canonical" not in skills or not isinstance(skills["canonical"], dict):
            errors.append("manifest missing `skills.canonical` object")
        if "command_policy" not in skills or not isinstance(
            skills["command_policy"], dict
        ):
            errors.append("manifest missing `skills.command_policy` object")

    if not isinstance(installation, dict) or not isinstance(
        installation.get("system_files"), dict
    ):
        errors.append("manifest missing `installation.system_files` object")

    if errors:
        return errors

    canonical_agents = set(agents["canonical"].keys())
    canonical_commands = set(commands["canonical"].keys())
    canonical_skills = set(skills["canonical"].keys())

    for command_name, config in commands["canonical"].items():
        owner = config.get("owner")
        if owner not in canonical_agents:
            errors.append(
                f"command `{command_name}` owner `{owner}` is not a canonical agent"
            )

    for skill_name, config in skills["canonical"].items():
        owners = config.get("owners")
        triggers = config.get("triggers")

        if not check_string_list(owners) or not owners:
            errors.append(f"skill `{skill_name}` must define non-empty `owners` list")
        else:
            unknown_owners = sorted(set(owners) - canonical_agents)
            if unknown_owners:
                errors.append(
                    f"skill `{skill_name}` has unknown owners: {', '.join(unknown_owners)}"
                )

        if not check_string_list(triggers) or not triggers:
            errors.append(f"skill `{skill_name}` must define non-empty `triggers` list")

    command_policy = skills["command_policy"]
    if set(command_policy.keys()) != canonical_commands:
        errors.append(
            "`skills.command_policy` keys must match canonical commands: "
            f"expected {sorted(canonical_commands)}, got {sorted(command_policy.keys())}"
        )
    for command_name, policy in command_policy.items():
        primary = policy.get("primary")
        optional = policy.get("optional")
        if primary not in canonical_skills:
            errors.append(
                f"command policy `{command_name}` references unknown primary skill `{primary}`"
            )
        if not check_string_list(optional):
            errors.append(f"command policy `{command_name}` optional must be string list")
            continue
        for skill_name in optional:
            if skill_name not in canonical_skills:
                errors.append(
                    f"command policy `{command_name}` references unknown optional skill `{skill_name}`"
                )
            if skill_name == primary:
                errors.append(
                    f"command policy `{command_name}` optional includes primary skill `{primary}`"
                )

    system_files = installation["system_files"]
    for platform in ["claude", "opencode"]:
        entries = system_files.get(platform)
        if not check_string_list(entries) or not entries:
            errors.append(
                f"installation.system_files.{platform} must be a non-empty string list"
            )

    return errors


def validate_template_references(repo_root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    def verify_entry(name: str, configured_path: Any, expected_path: str) -> None:
        if configured_path != expected_path:
            errors.append(
                f"`{name}` template mismatch: expected `{expected_path}`, got `{configured_path}`"
            )
            return
        target = repo_root / configured_path
        if not target.exists():
            errors.append(f"missing referenced template file: {configured_path}")

    for command_name, config in manifest["commands"]["canonical"].items():
        verify_entry(
            f"commands.canonical.{command_name}",
            config.get("template"),
            f"templates/shared/commands/crew/{command_name}.md",
        )

    for agent_name, config in manifest["agents"]["canonical"].items():
        verify_entry(
            f"agents.canonical.{agent_name}",
            config.get("template"),
            f"templates/shared/agents/crewai/{agent_name}.md",
        )

    for skill_name, config in manifest["skills"]["canonical"].items():
        verify_entry(
            f"skills.canonical.{skill_name}",
            config.get("template"),
            f"templates/shared/skills/{skill_name}/SKILL.md",
        )

    for workflow_name, config in manifest["workflows"]["canonical"].items():
        verify_entry(
            f"workflows.canonical.{workflow_name}",
            config.get("template"),
            f"templates/shared/workflows/{workflow_name}/SKILL.md",
        )

    for platform, entries in manifest["installation"]["system_files"].items():
        for entry in entries:
            path = repo_root / entry
            if not path.exists():
                errors.append(
                    f"installation.system_files.{platform} references missing file: {entry}"
                )

    return errors


def validate_generated_artifacts(repo_root: Path, manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    schema_path = repo_root / MANIFEST_SCHEMA_FILE
    if not schema_path.exists():
        errors.append(f"manifest schema file missing: {MANIFEST_SCHEMA_FILE}")

    expected_registry = dump_json(build_runtime_registry(manifest))
    registry_path = repo_root / RUNTIME_REGISTRY_FILE
    if not registry_path.exists():
        errors.append(f"generated runtime registry missing: {RUNTIME_REGISTRY_FILE}")
    else:
        actual_registry = registry_path.read_text(encoding="utf-8")
        if actual_registry != expected_registry:
            errors.append(
                f"{RUNTIME_REGISTRY_FILE} is out of sync with {MANIFEST_FILE}; run sync script"
            )

    install_path = repo_root / INSTALL_SCRIPT_FILE
    if not install_path.exists():
        errors.append(f"install script missing: {INSTALL_SCRIPT_FILE}")
    else:
        install_text = install_path.read_text(encoding="utf-8")
        expected_install_block = render_install_block(manifest)
        try:
            actual_install_block = extract_block(
                install_text,
                INSTALL_BLOCK_BEGIN,
                INSTALL_BLOCK_END,
            )
            if actual_install_block != expected_install_block:
                errors.append(
                    f"{INSTALL_SCRIPT_FILE} generated package block is out of sync with {MANIFEST_FILE}"
                )
        except ValueError as exc:
            errors.append(str(exc))

    readme_path = repo_root / README_FILE
    if not readme_path.exists():
        errors.append(f"README file missing: {README_FILE}")
    else:
        readme_text = readme_path.read_text(encoding="utf-8")

        readme_checks = [
            (
                README_WHATS_INSIDE_BEGIN,
                README_WHATS_INSIDE_END,
                render_readme_whats_inside_block(manifest),
                "README what's-inside block",
            ),
            (
                README_INSTALLER_COUNTS_BEGIN,
                README_INSTALLER_COUNTS_END,
                render_readme_installer_counts_block(manifest),
                "README installer-count block",
            ),
            (
                README_INDEX_BEGIN,
                README_INDEX_END,
                render_readme_index_block(manifest),
                "README index block",
            ),
        ]

        for begin, end, expected, label in readme_checks:
            try:
                actual = extract_block(readme_text, begin, end)
                if actual != expected:
                    errors.append(f"{label} is out of sync with {MANIFEST_FILE}")
            except ValueError as exc:
                errors.append(str(exc))

    return errors
