---
name: create-flow
description: Create a CrewAI Flow with state management, crew integration, and event-driven patterns. Use when asked to create a flow or multi-crew orchestration.
context: fork
agent: general-purpose
skills:
  - flows
  - core-build
---

# Create Flow Workflow

Create a CrewAI flow based on: $ARGUMENTS

## Your Process

### Stage 1: Analyze Requirements
1. Identify flow objective
2. Determine number of stages
3. Identify crews to integrate
4. Determine state requirements
5. Identify routing/conditional logic needed

### Stage 2: Design Flow Architecture
1. Define flow state model (Pydantic)
2. Design stage sequence
3. Plan crew integration points
4. Design routing logic if needed
5. Plan error handling

### Stage 3: Generate Flow Code
1. Generate state model class
2. Generate flow class with decorators
3. Generate crew integration code
4. Generate main.py entry point
5. Generate visualization code

### Stage 4: Generate Supporting Files
1. Generate pyproject.toml
2. Generate README.md
3. Create directory structure
4. Generate .env template

### Stage 5: Validate and Present
1. Validate flow structure
2. Generate flow diagram
3. Present complete flow
4. Ask for confirmation

## Output Format

```
## Flow Created: {flow_name}

### Flow Diagram
```
{ascii_or_mermaid_diagram}
```

### State Model
```python
{state_model}
```

### Flow Implementation
```python
{flow_code}
```

### Crews Integrated
- {crew_1}: {purpose}
- {crew_2}: {purpose}

### Files to Create
- src/{flow_name}/main.py
- src/{flow_name}/crews/{crew}/...

**Create these files? [y/n]**
```

## Flow Patterns

### Linear Flow
```python
class LinearFlow(Flow):
    @start()
    def step_one(self):
        return "data"
    
    @listen(step_one)
    def step_two(self, data):
        return process(data)
    
    @listen(step_two)
    def step_three(self, data):
        return finalize(data)
```

### Router Flow
```python
class RouterFlow(Flow):
    @start()
    def analyze(self):
        return self.state.input
    
    @router(analyze)
    def route(self):
        if self.state.score > 80:
            return "high_quality"
        return "needs_review"
    
    @listen("high_quality")
    def publish(self):
        pass
    
    @listen("needs_review")
    def revise(self):
        pass
```

### Parallel Flow
```python
class ParallelFlow(Flow):
    @start()
    def trigger(self):
        pass
    
    @listen(trigger)
    def task_a(self):
        return "result_a"
    
    @listen(trigger)
    def task_b(self):
        return "result_b"
    
    @listen(and_(task_a, task_b))
    def aggregate(self):
        return combine_results()
```

### Crew Integration Flow
```python
class CrewFlow(Flow[MyState]):
    @start()
    def prepare(self):
        self.state.topic = "AI trends"
    
    @listen(prepare)
    def run_research(self):
        result = ResearchCrew().crew().kickoff(
            inputs={"topic": self.state.topic}
        )
        self.state.research = result.raw
    
    @listen(run_research)
    def run_writing(self):
        result = WritingCrew().crew().kickoff(
            inputs={"research": self.state.research}
        )
        self.state.output = result.raw
```

## State Management

### Structured State (Recommended)
```python
from pydantic import BaseModel

class MyFlowState(BaseModel):
    id: str = ""
    input_data: str = ""
    processed_result: str = ""
    status: str = "pending"

class MyFlow(Flow[MyFlowState]):
    @start()
    def begin(self):
        self.state.status = "processing"
```

### Flow Persistence
```python
from crewai.flow.flow import Flow, persist

@persist
class PersistentFlow(Flow[MyState]):
    pass
```

## Success Criteria
- [ ] Flow state model is well-defined
- [ ] All stages have clear purposes
- [ ] Crew integrations are correct
- [ ] Routing logic is sound
- [ ] Error handling is included
- [ ] Visualization works
- [ ] User has confirmed file creation
