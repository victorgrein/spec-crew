#!/usr/bin/env python3
"""Validate canonical command smoke scenarios and enforce pass-rate threshold."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


INVOCATION_PATTERN = re.compile(r"^/crew\s+([a-z][a-z-]*)\b")
DEFAULT_MINIMUM_PASS_RATE = 0.95


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_command(invocation: str) -> str | None:
    match = INVOCATION_PATTERN.search(invocation.strip())
    if not match:
        return None
    return match.group(1)


def evaluate_case(
    case: dict,
    canonical_commands: set[str],
    owner_map: dict[str, str],
    commands_dir: Path,
) -> tuple[bool, str]:
    case_id = case.get("id")
    if not case_id:
        return False, "case missing `id`"

    invocation = case.get("invocation", "")
    invoked = parse_command(invocation)
    if not invoked:
        return False, "invalid `/crew ...` invocation"

    if invoked not in canonical_commands:
        return False, f"expected canonical invocation, got `{invoked}`"

    expected_command = case.get("expected_command")
    if expected_command and invoked != expected_command:
        return False, f"invoked command `{invoked}` != expected `{expected_command}`"

    expected_owner = case.get("expected_owner")
    actual_owner = owner_map.get(invoked)
    if expected_owner and actual_owner != expected_owner:
        return False, f"owner `{actual_owner}` != expected `{expected_owner}`"

    template_path = commands_dir / f"{invoked}.md"
    if not template_path.exists():
        return False, f"missing template `{template_path.name}`"

    return True, "ok"


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    registry_path = repo_root / "toolkit" / "registry.json"
    smoke_path = repo_root / "toolkit" / "cases" / "command-smoke.json"
    commands_dir = repo_root / "templates" / "shared" / "commands" / "crew"

    if not registry_path.exists():
        print(f"error: registry not found: {registry_path}")
        return 1
    if not smoke_path.exists():
        print(f"error: smoke case file not found: {smoke_path}")
        return 1
    if not commands_dir.exists():
        print(f"error: command templates not found: {commands_dir}")
        return 1

    registry = load_json(registry_path)
    smoke_cases = load_json(smoke_path)

    canonical_commands = set(registry["commands"]["canonical"].keys())
    owner_map = {
        name: cfg["owner"] for name, cfg in registry["commands"]["canonical"].items()
    }

    minimum_pass_rate = float(
        smoke_cases.get("minimum_pass_rate", DEFAULT_MINIMUM_PASS_RATE)
    )

    canonical_cases = smoke_cases.get("canonical_cases", [])

    if not isinstance(canonical_cases, list):
        print("Command smoke validation failed: `canonical_cases` must be an array.")
        return 1

    results: list[tuple[str, bool, str]] = []

    for case in canonical_cases:
        if not isinstance(case, dict):
            results.append(("canonical.invalid", False, "invalid canonical case entry"))
            continue
        case_id = case.get("id", "canonical.unknown")
        passed, message = evaluate_case(
            case,
            canonical_commands,
            owner_map,
            commands_dir,
        )
        results.append((case_id, passed, message))

    total = len(results)
    passed = sum(1 for _, ok, _ in results if ok)
    failed = total - passed
    pass_rate = (passed / total) if total else 0.0

    print("Command smoke pass-rate report:")
    print(f"- Total scenarios: {total}")
    print(f"- Passed: {passed}")
    print(f"- Failed: {failed}")
    print(f"- Smoke pass rate: {pass_rate * 100:.2f}%")
    print(f"- Required minimum: {minimum_pass_rate * 100:.2f}%")

    if failed:
        print("\nScenario failures:")
        for case_id, ok, message in results:
            if not ok:
                print(f"- {case_id}: {message}")

    if pass_rate + 1e-9 < minimum_pass_rate:
        print("\nCommand smoke pass-rate gate failed.")
        return 1

    print("\nCommand smoke pass-rate gate passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
