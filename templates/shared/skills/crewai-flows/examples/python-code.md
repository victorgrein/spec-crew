# CrewAI Flows - Python Code Examples

Python examples and implementation snippets for `crewai-flows`.

## Extracted Python Snippets

### Python Example 1

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

### Python Example 2

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

### Python Example 3

```python
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

class ReviewFlowState(BaseModel):
    content: str = ""
    quality_score: int = 0
    final_content: str = ""

class ReviewFlow(Flow[ReviewFlowState]):
    @start()
    def generate_content(self):
        self.state.content = "Generated content..."
        return self.state.content
    
    @listen(generate_content)
    def assess_quality(self, content):
        self.state.quality_score = 85  # Example score
        return self.state.quality_score
    
    @router(assess_quality)
    def route_by_quality(self):
        if self.state.quality_score >= 80:
            return "publish"
        elif self.state.quality_score >= 60:
            return "revise"
        else:
            return "reject"
    
    @listen("publish")
    def publish_content(self):
        self.state.final_content = self.state.content
        print("Content published!")
        return self.state.final_content
    
    @listen("revise")
    def revise_content(self):
        self.state.content = "Revised content..."
        return self.state.content
    
    @listen("reject")
    def reject_content(self):
        print("Content rejected, starting over...")
        return None
```

### Python Example 4

```python
from crewai.flow.flow import Flow, listen, start, and_
from pydantic import BaseModel
from typing import List

class ParallelFlowState(BaseModel):
    topics: List[str] = []
    research_a: str = ""
    research_b: str = ""
    combined: str = ""

class ParallelFlow(Flow[ParallelFlowState]):
    @start()
    def begin(self):
        return self.state.topics
    
    @listen(begin)
    def research_topic_a(self, topics):
        self.state.research_a = f"Research on {topics[0]}"
        return self.state.research_a
    
    @listen(begin)
    def research_topic_b(self, topics):
        # Runs in parallel with research_topic_a
        self.state.research_b = f"Research on {topics[1]}"
        return self.state.research_b
    
    @listen(and_(research_topic_a, research_topic_b))
    def combine_research(self):
        # Runs after BOTH complete
        self.state.combined = f"{self.state.research_a}\n{self.state.research_b}"
        return self.state.combined
```

### Python Example 5

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

### Python Example 6

```python
class UnstructuredFlow(Flow):
    @start()
    def first_method(self):
        self.state['counter'] = 0
        self.state['message'] = "Hello"
```

### Python Example 7

```python
from crewai.flow.flow import Flow, persist

@persist  # Class-level persistence
class MyFlow(Flow[MyState]):
    @start()
    def initialize_flow(self):
        self.state.counter = 1
```

### Python Example 8

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

### Python Example 9

```python
flow = MyFlow()
flow.plot("my_flow_diagram")  # Generates HTML visualization
```

### Python Example 10

```python
from crewai.flow.flow import Flow, listen, start

class ExampleFlow(Flow):
    @start()
    def generate_city(self):
        print("Starting flow")
        return "New York"
```

### Python Example 11

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

### Python Example 12

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

### Python Example 13

```python
from crewai.flow.flow import Flow, listen, or_, start

@listen(or_(start_method, second_method))
def logger(self, result):
    print(f"Logger: {result}")
```

### Python Example 14

```python
from crewai.flow.flow import Flow, and_, listen, start

@listen(and_(start_method, second_method))
def logger(self):
    print(self.state)
```

### Python Example 15

```python
class StreamingFlow(Flow):
    stream = True

flow = StreamingFlow()
streaming = flow.kickoff()
for chunk in streaming:
    print(chunk.content, end="", flush=True)
result = streaming.result
```

### Python Example 16

```python
from crewai.flow.flow import Flow, listen, router, start
from pydantic import BaseModel

class ReviewFlowState(BaseModel):
    content: str = ""
    quality_score: int = 0
    final_content: str = ""

class ReviewFlow(Flow[ReviewFlowState]):
    @start()
    def generate_content(self):
        self.state.content = "Generated content..."
        return self.state.content
    
    @listen(generate_content)
    def assess_quality(self, content):
        self.state.quality_score = 85
        return self.state.quality_score
    
    @router(assess_quality)
    def route_by_quality(self):
        if self.state.quality_score >= 80:
            return "publish"
        elif self.state.quality_score >= 60:
            return "revise"
        else:
            return "reject"
    
    @listen("publish")
    def publish_content(self):
        self.state.final_content = self.state.content
        print("Content published!")
        return self.state.final_content
    
    @listen("revise")
    def revise_content(self):
        self.state.content = "Revised content..."
        return self.state.content
    
    @listen("reject")
    def reject_content(self):
        print("Content rejected, starting over...")
        return None
```

### Python Example 17

```python
from crewai.flow.flow import Flow, listen, start, and_
from pydantic import BaseModel
from typing import List

class ParallelFlowState(BaseModel):
    topics: List[str] = []
    research_a: str = ""
    research_b: str = ""
    combined: str = ""

class ParallelFlow(Flow[ParallelFlowState]):
    @start()
    def begin(self):
        return self.state.topics
    
    @listen(begin)
    def research_topic_a(self, topics):
        self.state.research_a = f"Research on {topics[0]}"
        return self.state.research_a
    
    @listen(begin)
    def research_topic_b(self, topics):
        self.state.research_b = f"Research on {topics[1]}"
        return self.state.research_b
    
    @listen(and_(research_topic_a, research_topic_b))
    def combine_research(self):
        self.state.combined = f"{self.state.research_a}\n{self.state.research_b}"
        return self.state.combined
```

### Python Example 18

```python
from crewai.flow.flow import Flow, listen, start, persist
from pydantic import BaseModel

class PersistentState(BaseModel):
    step: int = 0
    data: str = ""

@persist
class PersistentFlow(Flow[PersistentState]):
    @start()
    def step_one(self):
        self.state.step = 1
        self.state.data = "Step 1 complete"
        return self.state.data
    
    @listen(step_one)
    def step_two(self, data):
        self.state.step = 2
        self.state.data = "Step 2 complete"
        return self.state.data
```

### Python Example 19

```python
from crewai.flow.flow import Flow, listen, start
from crewai.flow.human_feedback import human_feedback, HumanFeedbackResult
from pydantic import BaseModel

class ApprovalFlowState(BaseModel):
    content: str = ""
    approved: bool = False

class ApprovalFlow(Flow[ApprovalFlowState]):
    @start()
    @human_feedback(
        message="Do you approve this content?",
        emit=["approved", "rejected", "revise"],
        llm="gpt-4o-mini"
    )
    def generate_content(self):
        self.state.content = "Generated content for review..."
        return self.state.content
    
    @listen("approved")
    def on_approval(self, result: HumanFeedbackResult):
        self.state.approved = True
        print(f"Approved! Feedback: {result.feedback}")
        return self.state.content
    
    @listen("rejected")
    def on_rejection(self, result: HumanFeedbackResult):
        print(f"Rejected. Reason: {result.feedback}")
        return None
    
    @listen("revise")
    def on_revise(self, result: HumanFeedbackResult):
        print(f"Revision requested: {result.feedback}")
        return self.state.content
```

### Python Example 20

```python
#!/usr/bin/env python
from my_flow.flow import MyFlow

def kickoff():
    """Run the flow."""
    flow = MyFlow()
    result = flow.kickoff(inputs={"topic": "AI trends"})
    print(f"Result: {result}")

def plot():
    """Generate flow visualization."""
    flow = MyFlow()
    flow.plot("my_flow_diagram")

if __name__ == "__main__":
    kickoff()
```
