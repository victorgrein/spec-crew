# CrewAI Optimization - Basic Setup

Minimal setup path for `crewai-optimization` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

```python
result = crew.kickoff(inputs={...})
print(f"Token Usage: {crew.usage_metrics}")
print(f"Execution Time: {execution_time}")
```

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
