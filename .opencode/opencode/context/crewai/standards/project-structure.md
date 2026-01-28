# CrewAI Project Structure Standards

## Overview

Standard project structures for CrewAI crews and flows.

## Crew Project Structure

```
my_crew/
├── src/
│   └── my_crew/
│       ├── __init__.py
│       ├── main.py              # Entry point
│       ├── crew.py              # Crew definition
│       ├── config/
│       │   ├── agents.yaml      # Agent configurations
│       │   └── tasks.yaml       # Task configurations
│       └── tools/
│           ├── __init__.py
│           └── custom_tool.py   # Custom tools
├── tests/
│   ├── __init__.py
│   └── test_crew.py
├── output/                      # Generated outputs
├── pyproject.toml
├── README.md
├── .env                         # Environment variables
└── .gitignore
```

## Flow Project Structure

```
my_flow/
├── src/
│   └── my_flow/
│       ├── __init__.py
│       ├── main.py              # Flow entry point
│       ├── crews/
│       │   ├── __init__.py
│       │   ├── research_crew/
│       │   │   ├── __init__.py
│       │   │   ├── config/
│       │   │   │   ├── agents.yaml
│       │   │   │   └── tasks.yaml
│       │   │   └── research_crew.py
│       │   └── writing_crew/
│       │       ├── __init__.py
│       │       ├── config/
│       │       │   ├── agents.yaml
│       │       │   └── tasks.yaml
│       │       └── writing_crew.py
│       └── tools/
│           ├── __init__.py
│           └── custom_tool.py
├── tests/
├── output/
├── pyproject.toml
├── README.md
├── .env
└── .gitignore
```

## File Contents

### main.py (Crew)

```python
#!/usr/bin/env python
from my_crew.crew import MyCrew

def kickoff():
    """Run the crew."""
    inputs = {
        'topic': 'AI trends'
    }
    MyCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    kickoff()
```

### main.py (Flow)

```python
#!/usr/bin/env python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from .crews.research_crew.research_crew import ResearchCrew

class MyFlowState(BaseModel):
    topic: str = ""
    research: str = ""

class MyFlow(Flow[MyFlowState]):
    @start()
    def begin(self):
        return {"topic": self.state.topic}
    
    @listen(begin)
    def run_research(self, inputs):
        result = ResearchCrew().crew().kickoff(inputs=inputs)
        self.state.research = result.raw
        return result

def kickoff():
    flow = MyFlow()
    flow.kickoff(inputs={"topic": "AI trends"})

def plot():
    flow = MyFlow()
    flow.plot("my_flow")

if __name__ == "__main__":
    kickoff()
```

### crew.py

```python
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool

@CrewBase
class MyCrew:
    """My crew description."""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

### config/agents.yaml

```yaml
researcher:
  role: >
    {topic} Research Analyst
  goal: >
    Find comprehensive, accurate information about {topic}
  backstory: >
    Expert researcher with years of experience finding
    and synthesizing information from diverse sources.
```

### config/tasks.yaml

```yaml
research_task:
  description: >
    Research {topic} thoroughly. Find key facts, recent
    developments, and expert opinions.
  expected_output: >
    Comprehensive research report with key findings,
    sources cited, and relevant data points.
  agent: researcher
```

### pyproject.toml

```toml
[project]
name = "my_crew"
version = "0.1.0"
description = "My CrewAI project"
requires-python = ">=3.10"
dependencies = [
    "crewai>=0.100.0",
    "crewai-tools>=0.17.0",
]

[project.scripts]
kickoff = "my_crew.main:kickoff"

[tool.crewai]
type = "crew"

### pyproject.toml (Flow)

```toml
[project]
name = "my_flow"
version = "0.1.0"
description = "My CrewAI Flow"
requires-python = ">=3.10"
dependencies = [
    "crewai>=0.100.0",
]

[project.scripts]
kickoff = "my_flow.main:kickoff"
plot = "my_flow.main:plot"

[tool.crewai]
type = "flow"
```
```

### .env

```env
OPENAI_API_KEY=sk-...
SERPER_API_KEY=...
```

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/

# Environment
.env

# Output
output/

# IDE
.idea/
.vscode/

# OS
.DS_Store
```

## Directory Purposes

| Directory | Purpose |
|-----------|---------|
| `src/` | Source code |
| `config/` | YAML configurations |
| `tools/` | Custom tools |
| `tests/` | Test files |
| `output/` | Generated outputs |

## Best Practices

1. **Keep configs in YAML**: Easier to maintain and modify
2. **Separate tools**: Custom tools in dedicated directory
3. **Use __init__.py**: Proper Python package structure
4. **Output directory**: Keep generated files organized
5. **Environment variables**: Never commit .env files
6. **Tests**: Include basic tests for crews
