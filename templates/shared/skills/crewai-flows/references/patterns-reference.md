# CrewAI Flows - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-flows`.

## Common Archetypes and Patterns

### Basic Flow Pattern

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class MyFlowState(BaseModel):
    input_data: str = ""
    result: str = ""

class MyFlow(Flow[MyFlowState]):
    @start()
    def begin(self):
        return self.state.input_data
    
    @listen(begin)
    def process(self, data):
        self.state.result = f"Processed: {data}"
        return self.state.result

def kickoff():
    flow = MyFlow()
    result = flow.kickoff(inputs={"input_data": "test"})
    print(result)
```

### Flow with Crew Integration

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from .crews.research_crew.research_crew import ResearchCrew
from .crews.writing_crew.writing_crew import WritingCrew

class ContentFlowState(BaseModel):
    topic: str = ""
    research: str = ""
    article: str = ""

class ContentFlow(Flow[ContentFlowState]):
    @start()
    def prepare(self):
        print(f"Starting content flow for: {self.state.topic}")
        return {"topic": self.state.topic}
    
    @listen(prepare)
    def run_research(self, inputs):
        result = ResearchCrew().crew().kickoff(inputs=inputs)
        self.state.research = result.raw
        return {"topic": self.state.topic, "research": result.raw}
    
    @listen(run_research)
    def run_writing(self, inputs):
        result = WritingCrew().crew().kickoff(inputs=inputs)
        self.state.article = result.raw
        return result.raw

def kickoff():
    flow = ContentFlow()
    result = flow.kickoff(inputs={"topic": "AI trends"})
    print(f"Article: {result}")

def plot():
    flow = ContentFlow()
    flow.plot("content_flow")
```

### Best Practices

1. **Use Pydantic State**: Type-safe, validated state
2. **Clear Method Names**: Describe what each step does
3. **State Updates**: Update state in each method
4. **Error Handling**: Handle failures gracefully
5. **Visualization**: Use plot() for debugging
6. **Persistence**: Enable for long-running flows

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
