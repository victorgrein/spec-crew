# CrewAI Tasks

> Source: Official CrewAI Documentation

## Overview

A Task is a specific assignment completed by an Agent. Tasks provide all necessary details for execution, such as a description, the agent responsible, required tools, and expected output.

## Task Attributes

### Essential Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `description` | `str` | Clear, detailed description of what needs to be done |
| `expected_output` | `str` | Specific description of expected deliverable |
| `agent` | `Agent` | Agent responsible for the task |
| `name` | `str` | Identifier for the task |

### Context and Dependencies

| Attribute | Type | Description |
|-----------|------|-------------|
| `context` | `List[Task]` | Tasks whose output provides context |
| `tools` | `List[BaseTool]` | Task-specific tools (override agent tools) |

### Output Handling

| Attribute | Type | Description |
|-----------|------|-------------|
| `output_file` | `str` | Save output to file |
| `output_json` | `Type[BaseModel]` | Parse output as JSON |
| `output_pydantic` | `Type[BaseModel]` | Parse output as Pydantic model |
| `markdown` | `bool` | False | Return output as Markdown |
| `create_directory` | `bool` | True | Create output file directory |

### Execution Settings

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `async_execution` | `bool` | False | Run asynchronously |
| `human_input` | `bool` | False | Require human approval |
| `callback` | `Callable` | None | Function called after completion |
| `config` | `Dict` | None | Task-specific configuration |
| `guardrail` | `Callable` | None | Validation function |
| `guardrails` | `List[Callable]` | None | List of validation functions |
| `guardrail_max_retries` | `int` | 3 | Retries on validation failure |

## Creating Tasks

### YAML Configuration (Recommended)

```yaml
# config/tasks.yaml
research_task:
  description: >
    Research the latest developments in {topic} from the past month.
    Focus on peer-reviewed sources and industry reports.
  expected_output: >
    A comprehensive report of 500-800 words covering:
    1) Key findings
    2) Market implications
    3) Recommended actions
    Use markdown formatting.
  agent: researcher

analysis_task:
  description: >
    Analyze the research findings and identify key patterns.
  expected_output: >
    An analysis report with insights and recommendations.
  agent: analyst
  context:
    - research_task
```

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

### Direct Code Definition

```python
from crewai import Task

research_task = Task(
    description="Research the latest AI developments",
    expected_output="A detailed report with key findings",
    agent=researcher,
    tools=[SerperDevTool()]
)

analysis_task = Task(
    description="Analyze the research findings",
    expected_output="Analysis with recommendations",
    agent=analyst,
    context=[research_task]  # Uses research_task output
)
```

## Task Patterns

### Research Task

```python
research_task = Task(
    description="""
    Research {topic} and gather comprehensive information from reliable sources.
    Include recent developments, key players, and market trends.
    """,
    expected_output="""
    A detailed research summary including:
    - Key findings (minimum 5 points)
    - Sources cited
    - Relevant data points and statistics
    """,
    agent=researcher,
    tools=[SerperDevTool(), WebsiteSearchTool()]
)
```

### Analysis Task

```python
analysis_task = Task(
    description="""
    Analyze the provided research and identify key patterns, insights,
    and actionable recommendations.
    """,
    expected_output="""
    An analysis report with:
    1) Key insights (3-5 points)
    2) Supporting evidence
    3) Actionable recommendations (3-5 items)
    """,
    agent=analyst,
    context=[research_task]
)
```

### Writing Task with Output File

```python
writing_task = Task(
    description="""
    Write a blog post about {topic} based on the research and analysis.
    Make it engaging and accessible to a general audience.
    """,
    expected_output="""
    A well-structured blog post of 800-1200 words in markdown format.
    Include an introduction, main sections, and conclusion.
    """,
    agent=writer,
    context=[research_task, analysis_task],
    output_file="output/blog_post.md"
)
```

### Structured Output Task

```python
from pydantic import BaseModel
from typing import List

class ResearchFindings(BaseModel):
    key_points: List[str]
    sources: List[str]
    confidence_score: float

extraction_task = Task(
    description="Extract structured data from the research",
    expected_output="Structured research findings",
    agent=analyst,
    output_pydantic=ResearchFindings
)
```

## Context Passing

Tasks can receive context from previous tasks:

```python
# Task 1 output becomes context for Task 2
task1 = Task(
    description="Research topic",
    expected_output="Research report",
    agent=researcher
)

task2 = Task(
    description="Analyze the research findings from the previous task",
    expected_output="Analysis report",
    agent=analyst,
    context=[task1]  # Receives task1's output
)

task3 = Task(
    description="Write based on research and analysis",
    expected_output="Final document",
    agent=writer,
    context=[task1, task2]  # Receives both outputs
)
```

## Async Execution

```python
# Independent tasks can run asynchronously
task1 = Task(
    description="Research topic A",
    agent=researcher,
    async_execution=True
)

task2 = Task(
    description="Research topic B",
    agent=researcher,
    async_execution=True
)

# This task waits for both
task3 = Task(
    description="Combine findings",
    agent=analyst,
    context=[task1, task2]
)
```

## Human Input

```python
review_task = Task(
    description="Review the generated content",
    expected_output="Approved content or revision requests",
    agent=reviewer,
    human_input=True  # Requires human approval
)
```

## Task Callbacks

```python
def task_completed(output):
    print(f"Task completed: {output.raw[:100]}...")
    # Log to database, send notification, etc.

task = Task(
    description="...",
    expected_output="...",
    agent=agent,
    callback=task_completed
)
```

## Best Practices

1. **Clear Descriptions**: Be specific about what needs to be done
2. **Measurable Outputs**: Define concrete, verifiable expected outputs
3. **Proper Context**: List all tasks whose output is needed
4. **Avoid Circular Dependencies**: Tasks can't depend on each other
5. **Use Variables**: Use `{variable}` for dynamic content
6. **Output Files**: Specify for tasks generating artifacts
7. **Structured Output**: Use Pydantic models for data extraction
