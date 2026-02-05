# CrewAI Tasks - Basic Setup

Minimal setup path for `crewai-tasks` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

```python
@task
def research_task(self) -> Task:
    return Task(config=self.tasks_config['research_task'])

@task
def analysis_task(self) -> Task:
    return Task(
        config=self.tasks_config['analysis_task'],
        context=[self.research_task()]
    )
```

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
