# CrewAI Migration Process

## Overview

Guide for migrating CrewAI projects to standard flow structure and refactoring existing codebases.

## Migration Types

### 1. Crew to Flow Migration

Convert standalone crew to flow-based architecture.

### 2. Code to YAML Migration

Move inline definitions to YAML configuration.

### 3. Monolithic to Modular

Break large crew into smaller, reusable components.

### 4. Version Upgrade

Update to latest CrewAI version.

## Standard Project Structure

### Flow Project (Target)

```
my_project/
├── src/
│   └── my_project/
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
│       │       └── ...
│       └── tools/
│           ├── __init__.py
│           └── custom_tool.py
├── tests/
├── pyproject.toml
├── README.md
└── .env
```

## Crew to Flow Migration

### Step 1: Create Flow Project Structure

```bash
crewai create flow my_project
```

### Step 2: Move Existing Crew

```bash
# Create crew directory
mkdir -p src/my_project/crews/my_crew/config

# Move/copy crew files
cp old_project/crew.py src/my_project/crews/my_crew/my_crew.py
cp old_project/config/* src/my_project/crews/my_crew/config/
```

### Step 3: Update Crew Imports

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

### Step 4: Create Flow

```python
# main.py
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from .crews.my_crew.my_crew import MyCrew

class MyFlowState(BaseModel):
    topic: str = ""
    result: str = ""

class MyFlow(Flow[MyFlowState]):
    @start()
    def prepare_inputs(self):
        return {"topic": self.state.topic}
    
    @listen(prepare_inputs)
    def run_crew(self, inputs):
        result = MyCrew().crew().kickoff(inputs=inputs)
        self.state.result = result.raw
        return result

def kickoff():
    flow = MyFlow()
    flow.kickoff(inputs={"topic": "AI trends"})

def plot():
    flow = MyFlow()
    flow.plot("my_flow")
```

### Step 5: Update pyproject.toml

```toml
[tool.crewai]
type = "flow"

[project.scripts]
kickoff = "my_project.main:kickoff"
plot = "my_project.main:plot"
```

## Code to YAML Migration

### Before (Inline Code)

```python
researcher = Agent(
    role="Research Analyst",
    goal="Find accurate information",
    backstory="Expert researcher with attention to detail"
)

research_task = Task(
    description="Research the topic thoroughly",
    expected_output="Comprehensive research report",
    agent=researcher
)
```

### After (YAML + Decorators)

```yaml
# config/agents.yaml
researcher:
  role: >
    Research Analyst
  goal: >
    Find accurate information
  backstory: >
    Expert researcher with attention to detail
```

```yaml
# config/tasks.yaml
research_task:
  description: >
    Research the topic thoroughly
  expected_output: >
    Comprehensive research report
  agent: researcher
```

```python
@CrewBase
class MyCrew:
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
```

## Monolithic to Modular Migration

### Step 1: Identify Logical Groups

Group agents and tasks by responsibility:
- Research agents/tasks → research_crew
- Writing agents/tasks → writing_crew
- Analysis agents/tasks → analysis_crew

### Step 2: Extract Crews

Create separate crew for each group:

```
crews/
├── research_crew/
│   ├── config/
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   └── research_crew.py
├── writing_crew/
│   └── ...
└── analysis_crew/
    └── ...
```

### Step 3: Extract Shared Tools

```
tools/
├── __init__.py
├── search_tool.py
└── file_tool.py
```

### Step 4: Create Orchestrating Flow

```python
class MainFlow(Flow[MainState]):
    @start()
    def begin(self):
        pass
    
    @listen(begin)
    def run_research(self):
        return ResearchCrew().crew().kickoff(inputs={...})
    
    @listen(run_research)
    def run_analysis(self, research_result):
        return AnalysisCrew().crew().kickoff(inputs={...})
    
    @listen(run_analysis)
    def run_writing(self, analysis_result):
        return WritingCrew().crew().kickoff(inputs={...})
```

## Version Upgrade

### Step 1: Backup

```bash
cp -r my_project my_project_backup
```

### Step 2: Update Dependencies

```bash
uv add crewai@latest
uv add 'crewai[tools]'@latest
uv sync
```

### Step 3: Check Breaking Changes

Review CrewAI changelog for breaking changes.

### Step 4: Update Code

Apply necessary changes for new API.

### Step 5: Test

```bash
uv run pytest
crewai run
```

## Migration Checklist

- [ ] Backup existing project
- [ ] Create target structure
- [ ] Move/update crew files
- [ ] Update imports
- [ ] Create flow (if migrating to flow)
- [ ] Update pyproject.toml
- [ ] Test all functionality
- [ ] Update documentation
- [ ] Clean up old files
