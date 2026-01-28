# CrewAI Processes

> Source: Official CrewAI Documentation

## Overview

Processes in CrewAI define how tasks are executed and how agents collaborate. The process type determines the flow of work through the crew.

## Process Types

### Sequential Process (Default)

Tasks execute one after another in the order they are defined:

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential  # Default
)
```

**Characteristics:**
- Tasks run in defined order
- Each task's output becomes context for the next
- Simple, predictable flow
- Best for linear workflows

**Flow Diagram:**
```
Task 1 → Task 2 → Task 3 → Output
   ↓        ↓        ↓
Agent 1  Agent 2  Agent 3
```

### Hierarchical Process

A manager agent coordinates and delegates tasks to worker agents:

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, analyst],
    tasks=[research_task, write_task, analysis_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o"  # Required for hierarchical
)
```

**Characteristics:**
- Manager agent coordinates work
- Dynamic task delegation
- Manager validates outputs
- Best for complex, interdependent tasks

**Requirements:**
- Must specify `manager_llm` OR `manager_agent`

**Flow Diagram:**
```
        ┌─────────────────┐
        │  Manager Agent  │
        │   (Delegator)   │
        └────────┬────────┘
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Worker 1 │ │ Worker 2 │ │ Worker 3 │
└──────────┘ └──────────┘ └──────────┘
```

## Sequential Process Details

### Task Order

Tasks execute in the order they appear in the tasks list:

```python
crew = Crew(
    agents=[agent1, agent2, agent3],
    tasks=[
        task1,  # Executes first
        task2,  # Executes second (receives task1 output)
        task3   # Executes third (receives task1, task2 output)
    ],
    process=Process.sequential
)
```

### Context Passing

Each task can access outputs from previous tasks:

```python
task1 = Task(
    description="Research the topic",
    expected_output="Research findings",
    agent=researcher
)

task2 = Task(
    description="Analyze the research findings",
    expected_output="Analysis report",
    agent=analyst,
    context=[task1]  # Explicitly receive task1 output
)

task3 = Task(
    description="Write based on research and analysis",
    expected_output="Final document",
    agent=writer,
    context=[task1, task2]  # Receive both outputs
)
```

### When to Use Sequential

- Linear workflows with clear steps
- Each task depends on the previous
- Simple, predictable execution
- Debugging and testing

## Hierarchical Process Details

### Manager Configuration

**Option 1: Manager LLM**
```python
crew = Crew(
    agents=[worker1, worker2, worker3],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_llm="gpt-4o"  # CrewAI creates manager agent
)
```

**Option 2: Custom Manager Agent**
```python
manager = Agent(
    role="Project Manager",
    goal="Coordinate team to deliver high-quality results",
    backstory="Experienced manager skilled at delegation",
    allow_delegation=True
)

crew = Crew(
    agents=[worker1, worker2, worker3],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_agent=manager
)
```

### Manager Responsibilities

1. **Task Analysis**: Understand task requirements
2. **Delegation**: Assign tasks to appropriate agents
3. **Coordination**: Manage dependencies and order
4. **Validation**: Review and approve outputs
5. **Iteration**: Request revisions if needed

### When to Use Hierarchical

- Complex tasks requiring coordination
- Multiple specialists with different skills
- Tasks with unclear dependencies
- Need for quality validation
- Dynamic workflow decisions

## Comparison

| Aspect | Sequential | Hierarchical |
|--------|------------|--------------|
| **Complexity** | Simple | Complex |
| **Control** | Predictable | Dynamic |
| **Coordination** | Implicit (order) | Explicit (manager) |
| **Validation** | None built-in | Manager validates |
| **Best For** | Linear workflows | Complex projects |
| **Requirements** | None | manager_llm or manager_agent |
| **Token Usage** | Lower | Higher (manager overhead) |

## Process Selection Guide

### Use Sequential When:
- Tasks have clear, linear dependencies
- Order of execution is known upfront
- Simple workflows with 2-5 tasks
- Debugging or testing
- Cost optimization is priority

### Use Hierarchical When:
- Tasks are complex and interdependent
- Need dynamic task allocation
- Quality validation is important
- Multiple specialists collaborate
- Workflow decisions depend on outputs

## Example: Sequential Crew

```python
from crewai import Agent, Crew, Task, Process

researcher = Agent(role="Researcher", goal="Research topics", backstory="Expert")
writer = Agent(role="Writer", goal="Write content", backstory="Skilled writer")
editor = Agent(role="Editor", goal="Edit content", backstory="Detail-oriented")

research = Task(description="Research {topic}", expected_output="Findings", agent=researcher)
write = Task(description="Write article", expected_output="Draft", agent=writer, context=[research])
edit = Task(description="Edit article", expected_output="Final", agent=editor, context=[write])

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research, write, edit],
    process=Process.sequential,
    verbose=True
)

result = crew.kickoff(inputs={"topic": "AI trends"})
```

## Example: Hierarchical Crew

```python
from crewai import Agent, Crew, Task, Process

# Workers
researcher = Agent(role="Researcher", goal="Research", backstory="Expert researcher")
analyst = Agent(role="Analyst", goal="Analyze", backstory="Data analyst")
writer = Agent(role="Writer", goal="Write", backstory="Content writer")

# Tasks
research = Task(description="Research {topic}", expected_output="Findings", agent=researcher)
analyze = Task(description="Analyze data", expected_output="Analysis", agent=analyst)
write = Task(description="Write report", expected_output="Report", agent=writer)

# Hierarchical crew with manager
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research, analyze, write],
    process=Process.hierarchical,
    manager_llm="gpt-4o",
    verbose=True
)

result = crew.kickoff(inputs={"topic": "Market trends"})
```
