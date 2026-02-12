#!/usr/bin/env python3
"""Validate canonical agent prompts and prompt-size budgets."""

from __future__ import annotations

import json
import sys
from pathlib import Path


MAX_CANONICAL_LINES = 140
MAX_TOTAL_LINES = 700


def load_registry(repo_root: Path) -> dict:
    registry_path = repo_root / "toolkit" / "registry.json"
    return json.loads(registry_path.read_text(encoding="utf-8"))


def line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8").splitlines())


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    agents_dir = repo_root / "templates" / "shared" / "agents" / "crewai"
    registry = load_registry(repo_root)

    canonical_agents = sorted(registry["agents"]["canonical"].keys())
    expected_canonical = ["auditor", "builder", "docs", "flow"]

    errors: list[str] = []

    if canonical_agents != expected_canonical:
        errors.append(
            "canonical agent set mismatch: "
            f"expected {expected_canonical}, got {canonical_agents}"
        )

    canonical_total = 0

    for name in canonical_agents:
        path = agents_dir / f"{name}.md"
        if not path.exists():
            errors.append(
                f"missing canonical agent file: {path.relative_to(repo_root)}"
            )
            continue

        lines = line_count(path)
        canonical_total += lines
        if lines > MAX_CANONICAL_LINES:
            errors.append(
                f"canonical agent prompt too large ({lines} lines): {path.relative_to(repo_root)}"
            )

        content = path.read_text(encoding="utf-8")
        for required_tag in ["<ownership>", "<scope>", "<output_contract>"]:
            if required_tag not in content:
                errors.append(
                    f"canonical agent missing {required_tag}: {path.relative_to(repo_root)}"
                )

    total_lines = canonical_total
    if total_lines > MAX_TOTAL_LINES:
        errors.append(
            f"total agent prompt budget exceeded: {total_lines} > {MAX_TOTAL_LINES} lines"
        )

    existing_templates = {path.stem for path in agents_dir.glob("*.md")}
    unexpected_templates = sorted(existing_templates - set(canonical_agents))
    if unexpected_templates:
        errors.append(
            "unexpected non-canonical agent templates present: "
            + ", ".join(unexpected_templates)
        )

    if errors:
        print("Agent consolidation validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Agent consolidation validation passed.")
    print(f"Canonical agents: {len(canonical_agents)}")
    print(f"Canonical prompt lines: {canonical_total}")
    print(f"Total prompt lines: {total_lines}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
