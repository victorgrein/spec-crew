# Task Attributes Reference

Complete reference of all Task configuration attributes in CrewAI.

## Required Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `description` | str | - | Detailed task description including context and requirements |
| `expected_output` | str | - | Clear definition of what successful completion looks like |
| `agent` | str | - | Reference to the agent responsible for this task |

## Optional Attributes

### Execution Control

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `async_mode` | bool | False | Run task asynchronously |
| `timeout` | int | None | Maximum execution time in seconds |
| `max_retries` | int | 3 | Number of retries on failure |

### Output Configuration

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `output_file` | str | None | File path to save task output |
| `output_json` | str | None | JSON file path for structured output |
| `output_pydantic` | Type | None | Pydantic model class for validation |
| `markdown` | bool | False | Format output as markdown |
| `human_input` | bool | False | Pause for human review before completion |

### Context and Dependencies

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | List[str] | [] | References to tasks that must complete first |
| `callback` | Callable | None | Function called on task completion |

### Quality and Validation

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `guardrails` | List[str] | [] | Constraints and rules for output |
| `quality_check` | bool | False | Enable automated quality validation |
| `output_strict` | bool | False | Require exact format matching |

### Parallel Execution

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `parallel` | List[str] | [] | Tasks to run in parallel with this one |
| `max_workers` | int | 4 | Maximum parallel workers for async tasks |

## Attribute Details

### Description

Task descriptions should be:
- Clear and specific
- Include all necessary context
- Break complex tasks into steps
- Specify inputs and expected formats

Example:
```yaml
description: >
  Analyze Q3 sales data to identify trends:
  1. Load sales_data.csv from data/ directory
  2. Calculate total revenue by product category
  3. Identify top 5 performing products
  4. Compare month-over-month growth rates
  5. Highlight any anomalies or concerns
```

### Expected Output

Define exactly what successful completion looks like:
- Format specification
- Required sections
- Length constraints
- Quality indicators

Example:
```yaml
expected_output: >
  A markdown report containing:
  - Executive summary (150-200 words)
  - Revenue breakdown table
  - Top 5 products list with metrics
  - Growth rate analysis
  - Key recommendations (3-5 bullet points)
```

### Context Dependencies

Specify upstream tasks that must complete:

```yaml
context:
  - data_collection_task
  - validation_task
```

Rules:
- All context tasks must complete before execution
- Output from context tasks is available to current task
- Creates directed acyclic graph (DAG) of dependencies

### Output Pydantic Model

For structured outputs, define a Pydantic model:

```python
from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    summary: str
    key_findings: List[str]
    confidence_score: float
    recommendations: List[str]
```

Then reference in YAML:
```yaml
output_pydantic: AnalysisResult
```

### Guardrails

Define constraints on task outputs:

```yaml
guardrails:
  - Response must be under 1000 words
  - All numbers must include units
  - Cite sources for all external data
  - Use professional tone throughout
```

## Usage Examples

### Simple Task
```yaml
research_task:
  description: Research topic X
  expected_output: Summary of findings
  agent: researcher
```

### Complex Task with All Features
```yaml
comprehensive_task:
  description: >
    Multi-step analysis workflow...
  expected_output: >
    Detailed report with sections...
  agent: senior_analyst
  context:
    - data_prep_task
    - validation_task
  output_file: output/report.md
  output_pydantic: ReportSchema
  markdown: true
  guardrails:
    - Must include executive summary
    - All claims require citations
  timeout: 600
  max_retries: 5
```

### Async Task
```yaml
batch_task:
  description: Process batch of items
  expected_output: Results for all items
  agent: processor
  async_mode: true
  max_workers: 10
  timeout: 1200
```
