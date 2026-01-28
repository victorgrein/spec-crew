# CrewAI Domain Knowledge Navigation

## Overview

This directory contains comprehensive documentation of CrewAI concepts, extracted from official documentation and organized for quick reference.

## Concepts

### Core Components

| File | Description | When to Load |
|------|-------------|--------------|
| [flows.md](concepts/flows.md) | Flow architecture, decorators, state management | Creating/debugging flows |
| [crews.md](concepts/crews.md) | Crew configuration, processes, outputs | Creating/configuring crews |
| [agents.md](concepts/agents.md) | Agent attributes, archetypes, configuration | Designing agents |
| [tasks.md](concepts/tasks.md) | Task configuration, context passing, outputs | Designing tasks |
| [tools.md](concepts/tools.md) | Built-in tools, custom tool creation | Adding/creating tools |
| [llms.md](concepts/llms.md) | LLM providers, model selection, optimization | Configuring LLMs |

### Supporting Concepts

| File | Description | When to Load |
|------|-------------|--------------|
| [memory.md](concepts/memory.md) | Memory types, configuration, use cases | Enabling memory features |
| [processes.md](concepts/processes.md) | Sequential vs hierarchical processes | Choosing process type |
| [cli.md](concepts/cli.md) | CLI commands, project management | Project setup/management |

## Quick Reference

### Creating a Crew

Load: `crews.md`, `agents.md`, `tasks.md`

```python
from crewai import Agent, Crew, Task, Process

agent = Agent(role="...", goal="...", backstory="...")
task = Task(description="...", expected_output="...", agent=agent)
crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)
result = crew.kickoff()
```

### Creating a Flow

Load: `flows.md`, `crews.md`

```python
from crewai.flow.flow import Flow, listen, start

class MyFlow(Flow):
    @start()
    def begin(self):
        return "data"
    
    @listen(begin)
    def process(self, data):
        return f"processed {data}"

flow = MyFlow()
result = flow.kickoff()
```

### Adding Tools

Load: `tools.md`

```python
from crewai_tools import SerperDevTool

agent = Agent(
    role="Researcher",
    tools=[SerperDevTool()]
)
```

### Configuring LLMs

Load: `llms.md`

```python
agent = Agent(
    role="...",
    llm="gpt-4o",
    function_calling_llm="gpt-4o-mini"
)
```

## Context Loading Strategy

### Level 1 (Minimal)
- Single concept file for focused tasks
- Example: Just `agents.md` for agent design

### Level 2 (Standard)
- Related concept files
- Example: `crews.md` + `agents.md` + `tasks.md` for crew creation

### Level 3 (Comprehensive)
- All relevant files for complex operations
- Example: All concepts for migration or full system design

## File Sizes

All files are optimized for context efficiency:
- Each file: 100-200 lines
- Total domain knowledge: ~1500 lines
- Load only what's needed for the task
