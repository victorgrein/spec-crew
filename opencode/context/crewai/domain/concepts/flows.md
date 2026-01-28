# CrewAI Flows

> Source: Official CrewAI Documentation

## Overview

CrewAI Flows is a powerful feature designed to streamline the creation and management of AI workflows. Flows allow developers to combine and coordinate coding tasks and Crews efficiently, providing a robust framework for building sophisticated AI automations.

## Key Benefits

1. **Simplified Workflow Creation**: Easily chain together multiple Crews and tasks to create complex AI workflows
2. **State Management**: Flows make it super easy to manage and share state between different tasks
3. **Event-Driven Architecture**: Built on an event-driven model, allowing for dynamic and responsive workflows
4. **Flexible Control Flow**: Implement conditional logic, loops, and branching within your workflows

## Core Decorators

### @start()

The `@start()` decorator marks entry points for a Flow:
- Declare multiple unconditional starts: `@start()`
- Gate a start on a prior method or router label: `@start("method_or_label")`
- Provide a callable condition to control when a start should fire

```python
from crewai.flow.flow import Flow, listen, start

class ExampleFlow(Flow):
    @start()
    def generate_city(self):
        print("Starting flow")
        return "New York"
```

### @listen()

The `@listen()` decorator marks a method as a listener for the output of another task:

```python
# Listen by method name (string)
@listen("generate_city")
def generate_fun_fact(self, random_city):
    return f"Fun fact about {random_city}"

# Listen by method reference
@listen(generate_city)
def generate_fun_fact(self, random_city):
    return f"Fun fact about {random_city}"
```

### @router()

The `@router()` decorator defines conditional routing logic:

```python
@router(start_method)
def route_decision(self):
    if self.state.success_flag:
        return "success"
    else:
        return "failed"

@listen("success")
def success_path(self):
    print("Success!")

@listen("failed")
def failure_path(self):
    print("Failed!")
```

## Conditional Logic

### or_ Function

Trigger when ANY of the specified methods emit output:

```python
from crewai.flow.flow import Flow, listen, or_, start

@listen(or_(start_method, second_method))
def logger(self, result):
    print(f"Logger: {result}")
```

### and_ Function

Trigger only when ALL specified methods emit output:

```python
from crewai.flow.flow import Flow, and_, listen, start

@listen(and_(start_method, second_method))
def logger(self):
    print(self.state)
```

## State Management

### Unstructured State

Flexible, dynamic state without predefined schema:

```python
class UnstructuredFlow(Flow):
    @start()
    def first_method(self):
        self.state['counter'] = 0
        self.state['message'] = "Hello"
```

### Structured State (Recommended for Production)

Type-safe state using Pydantic models:

```python
from pydantic import BaseModel

class ExampleState(BaseModel):
    counter: int = 0
    message: str = ""

class StructuredFlow(Flow[ExampleState]):
    @start()
    def first_method(self):
        self.state.message = "Hello from structured flow"
        self.state.counter += 1
```

## Flow Persistence

Use `@persist` decorator for automatic state persistence:

```python
from crewai.flow.flow import Flow, persist

@persist  # Class-level persistence
class MyFlow(Flow[MyState]):
    @start()
    def initialize_flow(self):
        self.state.counter = 1

# Or method-level persistence
class AnotherFlow(Flow):
    @persist
    @start()
    def begin(self):
        self.state["runs"] = self.state.get("runs", 0) + 1
```

## Human-in-the-Loop

```python
from crewai.flow.human_feedback import human_feedback, HumanFeedbackResult

@start()
@human_feedback(
    message="Do you approve this content?",
    emit=["approved", "rejected"],
    llm="gpt-4o-mini",
    default_outcome="needs_revision",
)
def generate_content(self):
    return "Content to be reviewed..."

@listen("approved")
def on_approval(self, result: HumanFeedbackResult):
    print(f"Approved! Feedback: {result.feedback}")
```

## Adding Crews to Flows

```python
from crewai.flow.flow import Flow, listen, start
from .crews.poem_crew.poem_crew import PoemCrew

class PoemFlow(Flow[PoemState]):
    @start()
    def generate_sentence_count(self):
        self.state.sentence_count = randint(1, 5)

    @listen(generate_sentence_count)
    def generate_poem(self):
        result = PoemCrew().crew().kickoff(
            inputs={"sentence_count": self.state.sentence_count}
        )
        self.state.poem = result.raw
```

## Flow Project Structure

```
my_flow/
├── crews/
│   └── poem_crew/
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── poem_crew.py
├── tools/
│   └── custom_tool.py
├── main.py
├── pyproject.toml
└── README.md
```

## Running Flows

```bash
# Using CLI
crewai run
# or
crewai flow kickoff

# Using uv
uv run kickoff
```

## Visualization

```python
flow = MyFlow()
flow.plot("my_flow_diagram")  # Generates HTML visualization
```

## Streaming Execution

```python
class StreamingFlow(Flow):
    stream = True

flow = StreamingFlow()
streaming = flow.kickoff()
for chunk in streaming:
    print(chunk.content, end="", flush=True)
result = streaming.result
```
