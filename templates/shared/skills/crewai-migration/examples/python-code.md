# CrewAI Migration - Python Code Examples

Python examples and implementation snippets for `crewai-migration`.

## Extracted Python Snippets

### Python Example 1

```python
# my_crew.py
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class MyCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    
    # ... agent and task methods
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential
        )
```

### Python Example 2

```python
# main.py
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from .crews.my_crew.my_crew import MyCrew

class MyFlowState(BaseModel):
    topic: str = ""
    result: str = ""

class MyFlow(Flow[MyFlowState]):
    @start()
    def prepare_inputs(self):
        return {"topic": self.state.topic}
    
    @listen(prepare_inputs)
    def run_crew(self, inputs):
        result = MyCrew().crew().kickoff(inputs=inputs)
        self.state.result = result.raw
        return result

def kickoff():
    flow = MyFlow()
    flow.kickoff(inputs={"topic": "AI trends"})

def plot():
    flow = MyFlow()
    flow.plot("my_flow")
```

### Python Example 3

```python
researcher = Agent(
    role="Research Analyst",
    goal="Find accurate information",
    backstory="Expert researcher with attention to detail"
)

research_task = Task(
    description="Research the topic thoroughly",
    expected_output="Comprehensive research report",
    agent=researcher
)
```

### Python Example 4

```python
@CrewBase
class MyCrew:
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
```

### Python Example 5

```python
class MainFlow(Flow[MainState]):
    @start()
    def begin(self):
        pass
    
    @listen(begin)
    def run_research(self):
        return ResearchCrew().crew().kickoff(inputs={...})
    
    @listen(run_research)
    def run_analysis(self, research_result):
        return AnalysisCrew().crew().kickoff(inputs={...})
    
    @listen(run_analysis)
    def run_writing(self, analysis_result):
        return WritingCrew().crew().kickoff(inputs={...})
```
