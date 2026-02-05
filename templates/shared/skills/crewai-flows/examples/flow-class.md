# Flow Class Templates

## Basic Flow Template

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

## Flow with Crew Integration

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

## Flow with Router

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

## Flow with Parallel Execution

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

## Flow with Persistence

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

## Flow with Human Feedback

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

## Main Entry Point Template

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

## Best Practices

1. **Use Pydantic State**: Type-safe, validated state
2. **Clear Method Names**: Describe what each step does
3. **State Updates**: Update state in each method
4. **Error Handling**: Handle failures gracefully
5. **Visualization**: Use plot() for debugging
6. **Persistence**: Enable for long-running flows
