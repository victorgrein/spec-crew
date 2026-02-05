# CrewAI Processes - Python Code Examples

Python examples and implementation snippets for `crewai-processes`.

## Extracted Python Snippets

### Python Example 1

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential  # Default
)
```

### Python Example 2

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

### Python Example 3

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, analyst],
    tasks=[research_task, write_task, analysis_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o"  # Required for hierarchical
)
```

### Python Example 4

```python
crew = Crew(
    agents=[worker1, worker2, worker3],
    tasks=[task1, task2, task3],
    process=Process.hierarchical,
    manager_llm="gpt-4o"  # CrewAI creates manager agent
)
```

### Python Example 5

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

### Python Example 6

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

### Python Example 7

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

### Python Example 8

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
