# CrewAI Migration - Basic Setup

Minimal setup path for `crewai-migration` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

```python
# my_crew.py
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class MyCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    # ... agent and task methods
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential
        )
```

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
