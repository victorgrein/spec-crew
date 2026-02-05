# CrewAI Memory - Basic Setup

Minimal setup path for `crewai-memory` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

```python
from crewai import Agent

agent = Agent(
    role="Research Analyst",
    goal="Research and remember findings",
    backstory="Expert analyst with excellent memory",
    memory=True  # Enable memory
)
```

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
