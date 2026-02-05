# CrewAI Flows - Basic Setup

Minimal setup path for `crewai-flows` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

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

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
