#!/usr/bin/env python3
"""Run regression checks for canonical agent routing."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def route_query(query: str, keyword_map: dict[str, list[str]]) -> tuple[str | None, dict[str, int]]:
    text = query.lower()
    scores: dict[str, int] = {}
    for agent, keywords in keyword_map.items():
        scores[agent] = sum(text.count(keyword.lower()) for keyword in keywords)

    best_score = max(scores.values()) if scores else 0
    if best_score == 0:
        return None, scores

    winners = [agent for agent, score in scores.items() if score == best_score]
    if len(winners) != 1:
        return None, scores

    return winners[0], scores


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    cases_path = repo_root / "toolkit" / "cases" / "agent-routing.json"
    registry_path = repo_root / "toolkit" / "registry.json"

    cases_data = load_json(cases_path)
    registry = load_json(registry_path)

    errors: list[str] = []

    canonical_agents = sorted(cases_data["canonical_agents"])
    registry_agents = sorted(registry["agents"]["canonical"].keys())
    if canonical_agents != registry_agents:
        errors.append(
            "canonical agent mismatch between routing cases and toolkit registry: "
            f"cases={canonical_agents}, registry={registry_agents}"
        )

    command_expectations = cases_data["command_expectations"]
    registry_command_owners = {
        name: cfg["owner"] for name, cfg in registry["commands"]["canonical"].items()
    }
    for command_name, expected_owner in command_expectations.items():
        actual_owner = registry_command_owners.get(command_name)
        if actual_owner != expected_owner:
            errors.append(
                f"command owner mismatch for `{command_name}`: "
                f"expected `{expected_owner}`, got `{actual_owner}`"
            )

    keyword_map = cases_data["keyword_map"]
    for case in cases_data["cases"]:
        predicted, scores = route_query(case["query"], keyword_map)
        if predicted is None:
            errors.append(
                f"routing unresolved for case `{case['id']}`: scores={scores}"
            )
            continue

        if predicted != case["expected_primary"]:
            errors.append(
                f"routing mismatch for case `{case['id']}`: "
                f"expected `{case['expected_primary']}`, got `{predicted}` (scores={scores})"
            )

    orchestrator_files = [
        repo_root / "templates" / "claude" / "CLAUDE.md",
        repo_root / "templates" / "opencode" / "crewai-orchestrator.md",
    ]
    for file_path in orchestrator_files:
        text = file_path.read_text(encoding="utf-8")
        for canonical_agent in canonical_agents:
            if canonical_agent not in text:
                errors.append(
                    f"orchestrator routing missing `{canonical_agent}` in {file_path.relative_to(repo_root)}"
                )

    if errors:
        print("Agent routing regression failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Agent routing regression passed.")
    print(f"Validated routing cases: {len(cases_data['cases'])}")
    print(f"Validated command ownership checks: {len(command_expectations)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
