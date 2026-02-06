#!/usr/bin/env python3
"""Run representative end-to-end routing and policy scenarios."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


INVOCATION_PATTERN = re.compile(r"^/crew\s+([a-z][a-z-]*)\b")
DEFAULT_MINIMUM_PASS_RATE = 0.95


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_invocation(invocation: str) -> str | None:
    match = INVOCATION_PATTERN.search(invocation.strip())
    if not match:
        return None
    return match.group(1)


def run_scenario(
    scenario: dict,
    manifest: dict,
    repo_root: Path,
) -> tuple[bool, str]:
    invocation = scenario.get("invocation", "")
    expected_command = scenario.get("expected_command")
    expected_owner = scenario.get("expected_owner")
    expected_primary_skill = scenario.get("expected_primary_skill")
    required_optional_skills = scenario.get("required_optional_skills", [])

    if not isinstance(required_optional_skills, list):
        return False, "required_optional_skills must be a list"

    invoked_command = parse_invocation(invocation)
    if not invoked_command:
        return False, "invalid invocation"

    canonical_commands = manifest["commands"]["canonical"]

    if invoked_command not in canonical_commands:
        return False, f"expected canonical command, got `{invoked_command}`"

    if expected_command and invoked_command != expected_command:
        return False, f"resolved `{invoked_command}` != expected `{expected_command}`"

    owner = canonical_commands.get(invoked_command, {}).get("owner")
    if expected_owner and owner != expected_owner:
        return False, f"owner `{owner}` != expected `{expected_owner}`"

    command_policy = manifest["skills"]["command_policy"].get(invoked_command, {})
    primary_skill = command_policy.get("primary")
    optional_skills = command_policy.get("optional", [])

    if expected_primary_skill and primary_skill != expected_primary_skill:
        return (
            False,
            f"primary skill `{primary_skill}` != expected `{expected_primary_skill}`",
        )

    missing_optional = [
        skill for skill in required_optional_skills if skill not in optional_skills
    ]
    if missing_optional:
        return False, f"missing optional skills: {', '.join(missing_optional)}"

    command_template = repo_root / manifest["commands"]["canonical"][invoked_command]["template"]
    if not command_template.exists():
        return False, f"missing command template `{command_template}`"

    owner_template = repo_root / manifest["agents"]["canonical"][owner]["template"]
    if not owner_template.exists():
        return False, f"missing owner agent template `{owner_template}`"

    skill_template = repo_root / manifest["skills"]["canonical"][primary_skill]["template"]
    if not skill_template.exists():
        return False, f"missing primary skill template `{skill_template}`"

    return True, "ok"


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    manifest_path = repo_root / "toolkit" / "manifest.json"
    scenarios_path = repo_root / "toolkit" / "cases" / "e2e-scenarios.json"

    if not manifest_path.exists():
        print(f"error: manifest not found: {manifest_path}")
        return 1
    if not scenarios_path.exists():
        print(f"error: scenarios not found: {scenarios_path}")
        return 1

    manifest = load_json(manifest_path)
    scenarios_data = load_json(scenarios_path)
    scenarios = scenarios_data.get("scenarios", [])
    minimum_pass_rate = float(
        scenarios_data.get("minimum_pass_rate", DEFAULT_MINIMUM_PASS_RATE)
    )

    if not isinstance(scenarios, list) or not scenarios:
        print("E2E scenario validation failed: `scenarios` must be a non-empty array.")
        return 1

    results: list[tuple[str, bool, str]] = []
    for scenario in scenarios:
        if not isinstance(scenario, dict):
            results.append(("unknown", False, "scenario entry must be an object"))
            continue

        if "mode" in scenario:
            results.append(
                (
                    scenario.get("id", "unknown"),
                    False,
                    "`mode` is not supported; scenarios must be canonical-only",
                )
            )
            continue

        scenario_id = scenario.get("id", "unknown")
        passed, message = run_scenario(scenario, manifest, repo_root)
        results.append((scenario_id, passed, message))

    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = total - passed
    pass_rate = passed / total if total else 0.0

    print("Representative E2E scenario report:")
    print(f"- Total scenarios: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print(f"- Pass rate: {pass_rate * 100:.2f}%")
    print(f"- Required minimum: {minimum_pass_rate * 100:.2f}%")

    if failed:
        print("\nScenario failures:")
        for scenario_id, ok, message in results:
            if not ok:
                print(f"- {scenario_id}: {message}")

    if pass_rate + 1e-9 < minimum_pass_rate:
        print("\nRepresentative E2E scenario gate failed.")
        return 1

    print("\nRepresentative E2E scenario gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
