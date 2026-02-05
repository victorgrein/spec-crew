# CrewAI Crews - Python Code Examples

Python examples and implementation snippets for `crewai-crews`.

## Extracted Python Snippets

### Python Example 1

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

### Python Example 2

```python
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)
```

### Python Example 3

```python
crew = Crew(
    agents=[researcher, writer, analyst],
    tasks=[research_task, write_task, analysis_task],
    process=Process.hierarchical,
    manager_llm="gpt-4o"  # Required for hierarchical
)
```

### Python Example 4

```python
result = crew.kickoff(inputs={"topic": "AI"})
result = crew.kickoff_for_each(inputs=[{"topic": "AI"}, {"topic": "ML"}])
```

### Python Example 5

```python
result = await crew.akickoff(inputs={"topic": "AI"})
results = await crew.akickoff_for_each(inputs=[...])
```

### Python Example 6

```python
result = await crew.kickoff_async(inputs={"topic": "AI"})
results = await crew.kickoff_for_each_async(inputs=[...])
```

### Python Example 7

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

### Python Example 8

```python
crew = Crew(
    agents=[...],
    tasks=[...],
    memory=True,  # Enable memory
    cache=True,   # Enable caching
    embedder={"provider": "openai"}
)
```

### Python Example 9

```python
crew.kickoff()
print(crew.usage_metrics)
# {'total_tokens': 15000, 'prompt_tokens': 12000, ...}
```

### Python Example 10

```python
crew = Crew(
    agents=[...],
    output_log_file="logs.json"  # or "logs.txt" or True
)
```

### Python Example 11

```python
crew_output = crew.kickoff()
print(f"Raw: {crew_output.raw}")
print(f"Token Usage: {crew_output.token_usage}")
```
