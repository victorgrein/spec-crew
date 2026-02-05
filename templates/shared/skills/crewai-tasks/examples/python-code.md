# CrewAI Tasks - Python Code Examples

Python examples and implementation snippets for `crewai-tasks`.

## Extracted Python Snippets

### Python Example 1

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

### Python Example 2

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

### Python Example 3

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

### Python Example 4

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

### Python Example 5

```python
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

### Python Example 6

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

### Python Example 7

```python
review_task = Task(
    description="Review the generated content",
    expected_output="Approved content or revision requests",
    agent=reviewer,
    human_input=True  # Requires human approval
)
```

### Python Example 8

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

### Python Example 9

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

### Python Example 10

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

### Python Example 11

```python
crew.kickoff(inputs={
    "topic": "AI trends",
    "audience": "executives",
    "focus_area": "business impact"
})
```
