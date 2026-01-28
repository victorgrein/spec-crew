# CrewAI CLI

> Source: Official CrewAI Documentation

## Overview

CrewAI provides a command-line interface (CLI) for creating, managing, and running CrewAI projects.

## Installation

CrewAI uses `uv` as its dependency management and package handling tool:

```bash
pip install crewai
```

## Project Commands

### Create New Project

```bash
# Create a new crew project
crewai create crew my_crew

# Create a new flow project
crewai create flow my_flow
```

**Generated Structure (Crew):**
```
my_crew/
├── src/
│   └── my_crew/
│       ├── __init__.py
│       ├── main.py
│       ├── crew.py
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── tools/
│           └── custom_tool.py
├── tests/
├── pyproject.toml
└── README.md
```

**Generated Structure (Flow):**
```
my_flow/
├── src/
│   └── my_flow/
│       ├── __init__.py
│       ├── main.py
│       ├── crews/
│       │   └── poem_crew/
│       │       ├── config/
│       │       │   ├── agents.yaml
│       │       │   └── tasks.yaml
│       │       └── poem_crew.py
│       └── tools/
│           └── custom_tool.py
├── tests/
├── pyproject.toml
└── README.md
```

### Install Dependencies

```bash
crewai install
```

This runs `uv sync` to install all dependencies from `pyproject.toml`.

### Run Project

```bash
# Run crew or flow (auto-detects type)
crewai run

# Explicitly run flow
crewai flow kickoff
```

### Activate Virtual Environment

```bash
source .venv/bin/activate
```

## Dependency Management

### Add Dependencies

```bash
# Add a package
uv add package_name

# Add CrewAI tools
uv add 'crewai[tools]'

# Add specific version
uv add package_name@1.2.3
```

### Sync Dependencies

```bash
uv sync
```

### Update Dependencies

```bash
uv add crewai@latest
uv add 'crewai[tools]'@latest
```

## Debugging Commands

### View Task Outputs

```bash
crewai log-tasks-outputs
```

Shows the latest kickoff task IDs for replay.

### Replay from Task

```bash
crewai replay -t <task_id>
```

Replays execution from a specific task, retaining context from previous tasks.

## Flow Commands

### Kickoff Flow

```bash
crewai flow kickoff
```

### Plot Flow

```bash
crewai flow plot
```

Generates an HTML visualization of the flow.

## Running with uv

Alternative to `crewai run`:

```bash
# Run the project
uv run kickoff

# Run with specific inputs
uv run kickoff --topic "AI trends"

# Run tests
uv run pytest
```

## Project Configuration

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
plot = "my_crew.main:plot"

[tool.crewai]
type = "crew"  # or "flow"
```

### Environment Variables

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key
ANTHROPIC_API_KEY=your_api_key
SERPER_API_KEY=your_api_key
```

## Common Workflows

### Starting a New Crew Project

```bash
# Create project
crewai create crew my_project
cd my_project

# Install dependencies
crewai install

# Activate environment
source .venv/bin/activate

# Edit agents and tasks
# Edit src/my_project/config/agents.yaml
# Edit src/my_project/config/tasks.yaml

# Run
crewai run
```

### Starting a New Flow Project

```bash
# Create project
crewai create flow my_flow
cd my_flow

# Install dependencies
crewai install

# Activate environment
source .venv/bin/activate

# Edit flow and crews
# Edit src/my_flow/main.py
# Edit crews in src/my_flow/crews/

# Run
crewai run
```

### Adding a New Crew to Flow

```bash
# Copy existing crew as template
cp -r src/my_flow/crews/poem_crew src/my_flow/crews/new_crew

# Edit the new crew
# Edit config/agents.yaml
# Edit config/tasks.yaml
# Edit new_crew.py

# Import in main.py and add to flow
```

### Debugging a Crew

```bash
# Run with verbose output
# (Set verbose=True in crew definition)

# View task outputs
crewai log-tasks-outputs

# Replay from specific task
crewai replay -t <task_id>
```

## Tips

1. **Always use virtual environment**: `source .venv/bin/activate`
2. **Use uv for dependencies**: Faster than pip
3. **Check pyproject.toml**: Ensure type is set correctly (crew/flow)
4. **Use verbose mode**: Set `verbose=True` for debugging
5. **Save logs**: Use `output_log_file` for persistent logs
