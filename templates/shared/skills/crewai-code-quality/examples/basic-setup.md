# CrewAI Code Quality - Basic Setup

Minimal setup path for `crewai-code-quality` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

```python
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool

@CrewBase
class ResearchCrew:
    """Research crew for comprehensive topic analysis."""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        """Create the research analyst agent."""
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        """Create the research task."""
        return Task(config=self.tasks_config['research_task'])

    @crew
    def crew(self) -> Crew:
        """Create and configure the crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
