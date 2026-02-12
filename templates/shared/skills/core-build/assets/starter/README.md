# {Crew Name}

{Crew description}

## Setup

1. Copy `.env.example` to `.env` and fill in your API keys
2. Install dependencies: `pip install crewai crewai-tools`
3. Run the crew: `python main.py`

## Structure

- `config/agents.yaml` - Agent definitions
- `config/tasks.yaml` - Task definitions
- `crew.py` - Crew orchestration
- `main.py` - Entry point
- `output/` - Generated outputs

## Usage

```python
from crew import {CrewName}Crew

inputs = {"topic": "your topic here"}
result = {CrewName}Crew().crew().kickoff(inputs=inputs)
print(result)
```
