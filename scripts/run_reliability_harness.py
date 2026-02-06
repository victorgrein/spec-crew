#!/usr/bin/env python3
"""Run the phase-7 reliability harness checks with unified reporting."""

from __future__ import annotations

import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Check:
    name: str
    command: str


CHECKS: list[Check] = [
    Check("Manifest sync and asset integrity", "python3 scripts/validate_toolkit_manifest.py"),
    Check("Command references", "python3 scripts/validate_command_references.py"),
    Check("Markdown links", "python3 scripts/validate_markdown_links.py"),
    Check("Command surface contracts", "python3 scripts/validate_command_surface.py"),
    Check("Command smoke pass-rate gate", "python3 scripts/validate_command_smoke_rate.py"),
    Check("Representative E2E scenarios", "python3 scripts/validate_e2e_scenarios.py"),
    Check("Agent prompt budgets", "python3 scripts/validate_agent_consolidation.py"),
    Check("Agent routing regressions", "python3 scripts/validate_agent_routing.py"),
    Check("Skill prompt budgets", "python3 scripts/validate_skill_consolidation.py"),
    Check("Skill routing coverage", "python3 scripts/validate_skill_routing.py"),
]


def run_check(check: Check, repo_root: Path) -> tuple[bool, float, str]:
    started = time.monotonic()
    result = subprocess.run(
        shlex.split(check.command),
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    duration = time.monotonic() - started
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, duration, output.strip()


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    passed = 0
    failed = 0
    total_duration = 0.0

    print("Toolkit reliability harness")
    print(f"Checks: {len(CHECKS)}")

    for check in CHECKS:
        ok, duration, output = run_check(check, repo_root)
        total_duration += duration
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        else:
            failed += 1

        print(f"\n[{status}] {check.name} ({duration:.2f}s)")
        if output:
            for line in output.splitlines():
                print(f"  {line}")

    print("\nReliability harness summary")
    print(f"- Passed checks: {passed}")
    print(f"- Failed checks: {failed}")
    print(f"- Total checks: {len(CHECKS)}")
    print(f"- Total duration: {total_duration:.2f}s")

    if failed:
        print("\nReliability harness failed.")
        return 1

    print("\nReliability harness passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
