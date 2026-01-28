# CrewAI Code Quality Standards

## Overview

Standards for writing high-quality, maintainable CrewAI code.

## Project Structure

### Required Structure

```
my_project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       ├── crew.py (or crews/ for flows)
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── tools/
│           └── custom_tool.py
├── tests/
├── pyproject.toml
├── README.md
└── .env
```

### Naming Conventions

| Component | Convention | Example |
|-----------|------------|---------|
| Project | snake_case | `my_crew_project` |
| Crew class | PascalCase | `ResearchCrew` |
| Agent methods | snake_case | `research_analyst` |
| Task methods | snake_case | `research_task` |
| YAML keys | snake_case | `research_analyst` |
| Tool classes | PascalCase | `CustomSearchTool` |

## Agent Design Standards

### Role Definition

✅ **Good:**
```yaml
role: >
  Senior Data Research Analyst specializing in AI trends
```

❌ **Bad:**
```yaml
role: Researcher
```

### Goal Definition

✅ **Good:**
```yaml
goal: >
  Uncover comprehensive, accurate information about {topic}
  with focus on recent developments and expert opinions
```

❌ **Bad:**
```yaml
goal: Research stuff
```

### Backstory Definition

✅ **Good:**
```yaml
backstory: >
  You're a seasoned researcher with 10+ years of experience
  in technology analysis. Known for your ability to find
  hidden insights and present complex information clearly.
```

❌ **Bad:**
```yaml
backstory: Expert researcher
```

## Task Design Standards

### Description

✅ **Good:**
```yaml
description: >
  Research {topic} thoroughly using web searches and
  authoritative sources. Focus on:
  1. Recent developments (last 6 months)
  2. Key players and their contributions
  3. Market trends and predictions
  Include citations for all major claims.
```

❌ **Bad:**
```yaml
description: Research the topic
```

### Expected Output

✅ **Good:**
```yaml
expected_output: >
  A comprehensive research report (800-1200 words) containing:
  - Executive summary (100 words)
  - Key findings (5+ bullet points)
  - Detailed analysis (500-800 words)
  - Sources cited (minimum 3)
  Format: Markdown with headers
```

❌ **Bad:**
```yaml
expected_output: Research report
```

## Code Standards

### Crew Class

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

### Custom Tools

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class MyToolInput(BaseModel):
    """Input schema for MyTool."""
    query: str = Field(..., description="The search query")

class MyTool(BaseTool):
    """Custom tool for specific functionality."""
    
    name: str = "my_tool"
    description: str = """
    Use this tool when you need to [specific use case].
    Input: A search query string
    Output: Relevant results as formatted text
    """
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, query: str) -> str:
        """Execute the tool."""
        try:
            result = self._perform_search(query)
            return f"Results: {result}"
        except Exception as e:
            return f"Error: {str(e)}"
```

## Configuration Standards

### Environment Variables

```env
# Required
OPENAI_API_KEY=sk-...

# Optional
ANTHROPIC_API_KEY=sk-ant-...
SERPER_API_KEY=...

# Model defaults
OPENAI_MODEL_NAME=gpt-4o
```

### pyproject.toml

```toml
[project]
name = "my_crew"
version = "0.1.0"
description = "Description of what this crew does"
requires-python = ">=3.10"
dependencies = [
    "crewai>=0.100.0",
    "crewai-tools>=0.17.0",
]

[project.scripts]
kickoff = "my_crew.main:kickoff"

[tool.crewai]
type = "crew"  # or "flow"
```

## Error Handling Standards

### In Tools

```python
def _run(self, query: str) -> str:
    try:
        result = self._perform_operation(query)
        return result
    except ConnectionError as e:
        return f"Connection error: {str(e)}. Please try again."
    except ValueError as e:
        return f"Invalid input: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
```

### In Crews

```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        verbose=True,  # Enable for debugging
        max_rpm=30,    # Prevent rate limits
    )
```

## Documentation Standards

### README.md

Every project must include:
- Project description
- Installation instructions
- Configuration requirements
- Usage examples
- Architecture overview

### Code Comments

```python
@agent
def researcher(self) -> Agent:
    """
    Create the research analyst agent.
    
    This agent specializes in finding and synthesizing
    information from web sources. Uses SerperDevTool
    for web searches.
    
    Returns:
        Agent: Configured research agent
    """
    return Agent(...)
```

## Testing Standards

### Basic Test

```python
def test_crew_creation():
    """Test that crew can be created."""
    crew = MyCrew().crew()
    assert crew is not None
    assert len(crew.agents) > 0
    assert len(crew.tasks) > 0

def test_crew_execution():
    """Test crew execution with sample input."""
    crew = MyCrew().crew()
    result = crew.kickoff(inputs={"topic": "test"})
    assert result is not None
    assert result.raw != ""
```

## Checklist

- [ ] Project follows standard structure
- [ ] Naming conventions followed
- [ ] Agents have detailed roles, goals, backstories
- [ ] Tasks have clear descriptions and expected outputs
- [ ] Tools have proper error handling
- [ ] Environment variables documented
- [ ] README.md complete
- [ ] Tests included
