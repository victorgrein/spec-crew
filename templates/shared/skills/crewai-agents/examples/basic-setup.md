# CrewAI Agents - Basic Setup

Minimal setup path for `crewai-agents` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        tools=[SerperDevTool()],
        verbose=True
    )
```

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
