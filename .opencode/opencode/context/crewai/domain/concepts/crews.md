# CrewAI Crews

> Source: Official CrewAI Documentation

## Overview

A crew in CrewAI represents a collaborative group of agents working together to achieve a set of tasks. Each crew defines the strategy for task execution, agent collaboration, and the overall workflow.

## Crew Attributes

| Attribute | Parameter | Description |
|-----------|-----------|-------------|
| **Tasks** | `tasks` | A list of tasks assigned to the crew |
| **Agents** | `agents` | A list of agents that are part of the crew |
| **Process** | `process` | The process flow (sequential, hierarchical). Default: `sequential` |
| **Verbose** | `verbose` | Verbosity level for logging. Default: `False` |
| **Manager LLM** | `manager_llm` | LLM used by manager in hierarchical process. **Required for hierarchical** |
| **Manager Agent** | `manager_agent` | Custom agent as manager |
| **Function Calling LLM** | `function_calling_llm` | LLM for tool calling (overrides agent LLMs) |
| **Max RPM** | `max_rpm` | Maximum requests per minute (overrides agent settings) |
| **Memory** | `memory` | Enable execution memories (short-term, long-term, entity) |
| **Cache** | `cache` | Cache tool execution results. Default: `True` |
| **Embedder** | `embedder` | Embedder configuration. Default: `{"provider": "openai"}` |
| **Planning** | `planning` | Enable planning before each iteration |
| **Planning LLM** | `planning_llm` | LLM for AgentPlanner |
| **Knowledge Sources** | `knowledge_sources` | Knowledge sources accessible to all agents |
| **Stream** | `stream` | Enable streaming output. Default: `False` |
| **Output Log File** | `output_log_file` | Save logs to file (`.txt` or `.json`) |
| **Config** | `config` | Optional configuration settings |
| **Step Callback** | `step_callback` | Function called after each agent step |
| **Task Callback** | `task_callback` | Function called after each task completion |
| **Share Crew** | `share_crew` | Share crew data with CrewAI team |
| **Prompt File** | `prompt_file` | Path to prompt JSON file |

## Creating Crews

### YAML Configuration (Recommended)

```yaml
# config/agents.yaml
researcher:
  role: >
    {topic} Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}.
```

```yaml
# config/tasks.yaml
research_task:
  description: >
    Research the latest developments in {topic}
  expected_output: >
    A comprehensive report on {topic}
  agent: researcher
```

```python
from crewai import Agent, Crew, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class ResearchCrew:
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

### Decorators

- `@CrewBase`: Marks class as crew base
- `@agent`: Denotes method returning Agent
- `@task`: Denotes method returning Task
- `@crew`: Denotes method returning Crew
- `@before_kickoff`: Execute before crew starts
- `@after_kickoff`: Execute after crew finishes

## Process Types

### Sequential Process

Tasks execute one after another in order:

```python
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)
```

### Hierarchical Process

Manager agent coordinates and delegates:

```python
crew = Crew(
    agents=[researcher, writer, analyst],
    tasks=[research_task, write_task, analysis_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o"  # Required for hierarchical
)
```

## Crew Output

The `CrewOutput` class provides structured access to results:

| Attribute | Type | Description |
|-----------|------|-------------|
| `raw` | `str` | Raw output string |
| `pydantic` | `Optional[BaseModel]` | Structured Pydantic output |
| `json_dict` | `Optional[Dict]` | JSON dictionary output |
| `tasks_output` | `List[TaskOutput]` | Individual task outputs |
| `token_usage` | `Dict[str, Any]` | Token usage summary |

```python
crew_output = crew.kickoff()
print(f"Raw: {crew_output.raw}")
print(f"Token Usage: {crew_output.token_usage}")
```

## Kickoff Methods

### Synchronous

```python
result = crew.kickoff(inputs={"topic": "AI"})
result = crew.kickoff_for_each(inputs=[{"topic": "AI"}, {"topic": "ML"}])
```

### Asynchronous (Native)

```python
result = await crew.akickoff(inputs={"topic": "AI"})
results = await crew.akickoff_for_each(inputs=[...])
```

### Asynchronous (Thread-based)

```python
result = await crew.kickoff_async(inputs={"topic": "AI"})
results = await crew.kickoff_for_each_async(inputs=[...])
```

## Streaming Execution

```python
crew = Crew(
    agents=[researcher],
    tasks=[task],
    stream=True
)

streaming = crew.kickoff(inputs={"topic": "AI"})
for chunk in streaming:
    print(chunk.content, end="", flush=True)
result = streaming.result
```

## Memory and Cache

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,  # Enable memory
    cache=True,   # Enable caching
    embedder={"provider": "openai"}
)
```

## Usage Metrics

```python
crew.kickoff()
print(crew.usage_metrics)
# {'total_tokens': 15000, 'prompt_tokens': 12000, ...}
```

## Logging

```python
crew = Crew(
    agents=[...],
    output_log_file="logs.json"  # or "logs.txt" or True
)
```

## Replay from Task

```bash
# View task IDs
crewai log-tasks-outputs

# Replay from specific task
crewai replay -t <task_id>
```
