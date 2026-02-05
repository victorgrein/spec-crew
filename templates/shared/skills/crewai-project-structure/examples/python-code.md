# CrewAI Project Structure - Python Code Examples

Python examples and implementation snippets for `crewai-project-structure`.

## Extracted Python Snippets

### Python Example 1

```python
#!/usr/bin/env python
from my_crew.crew import MyCrew

def kickoff():
    """Run the crew."""
    inputs = {
        'topic': 'AI trends'
    }
    MyCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    kickoff()
```

### Python Example 2

```python
#!/usr/bin/env python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from .crews.research_crew.research_crew import ResearchCrew

class MyFlowState(BaseModel):
    topic: str = ""
    research: str = ""

class MyFlow(Flow[MyFlowState]):
    @start()
    def begin(self):
        return {"topic": self.state.topic}
    
    @listen(begin)
    def run_research(self, inputs):
        result = ResearchCrew().crew().kickoff(inputs=inputs)
        self.state.research = result.raw
        return result

def kickoff():
    flow = MyFlow()
    flow.kickoff(inputs={"topic": "AI trends"})

def plot():
    flow = MyFlow()
    flow.plot("my_flow")

if __name__ == "__main__":
    kickoff()
```

### Python Example 3

```python
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool

@CrewBase
class MyCrew:
    """My crew description."""
    
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
