# CrewAI Best Practices

Comprehensive guide for building high-quality CrewAI applications.

## Core Principles

1. **Keep architecture declarative**: agents and tasks in YAML, wiring in minimal Python.
2. **Specialize agents clearly** (role, goal, backstory) and avoid role overlap.
3. **Make each task single-purpose** with explicit expected output and context.
4. **Use `sequential` process by default**; adopt `hierarchical` only for true manager-led delegation.
5. **Validate outputs** with guardrails or typed schemas when correctness matters.

### Flow-Ready Crew Architecture

- Keep crew outputs structured so Flows can consume them reliably.
- Define stable input variable names in YAML for reuse across crews and flow stages.
- Avoid embedding agent prompt logic directly in Python constructors.

## Agent Design Principles

### 1. Clear Role Definition
- **Be specific**: Define expertise level and domain
- **Include unique qualities**: What makes this agent special?
- **Keep it focused**: One primary responsibility per agent

```yaml
# Good
role: Senior Python Developer specializing in FastAPI and async programming

# Bad
role: Developer
```

### 2. Actionable Goals
- **Measurable outcomes**: Define what success looks like
- **Time-bounded**: Include implicit time constraints
- **Achievable**: Match agent capabilities to goal complexity

```yaml
# Good
goal: Build a REST API with authentication, rate limiting, and 
      comprehensive error handling that can handle 1000 concurrent users

# Bad
goal: Create an API
```

### 3. Rich Backstories
- **Professional history**: Years of experience, notable companies
- **Working style**: How they approach problems
- **Communication preferences**: Tone, detail level, format preferences

```yaml
# Good
backstory: |
  You are a senior developer with 10 years of experience.
  You've led engineering teams at startups and Fortune 500s.
  You write clean, documented code and prefer simple solutions.
  You're excellent at explaining technical concepts to non-technical stakeholders.

# Bad
backstory: You are a good developer.
```

## Task Design Patterns

### 1. Single Responsibility
Each task should do ONE thing well. Avoid multi-purpose tasks.

```yaml
# Good - Separate concerns
research_task:
  description: Research the topic and compile findings
  
analysis_task:
  description: Analyze the research findings
  
report_task:
  description: Write final report based on analysis

# Bad - Too many responsibilities
task:
  description: Research, analyze, and write a report
```

### 2. Explicit Expected Outputs
Define exactly what completion looks like:

```yaml
expected_output: |
  A markdown report containing:
  1. Executive summary (150-200 words)
  2. Key findings (5-7 bullet points)
  3. Recommendations (3-5 actionable items)
  4. Risk assessment table
```

### 3. Context Dependencies
Use context to build data pipelines:

```yaml
# Data flows: collection -> cleaning -> analysis -> report
collection_task:
  description: Collect raw data
  
cleaning_task:
  description: Clean the collected data
  context:
    - collection_task
    
analysis_task:
  description: Analyze cleaned data
  context:
    - cleaning_task
    
report_task:
  description: Create final report
  context:
    - analysis_task
```

### 4. Guardrails for Quality
Add constraints to ensure consistent quality:

```yaml
guardrails:
  - Response must be 500-1000 words
  - All claims must include citations
  - Use professional tone throughout
  - Include at least 3 concrete examples
```

## Process Selection Guide

### Choose Sequential When:
- Simple linear workflow
- Clear task dependencies
- No need for oversight
- Straightforward automation

**Example:** Data ETL pipeline (Extract → Transform → Load)

### Choose Hierarchical When:
- Complex multi-step project
- Quality review needed
- Dynamic task assignment
- Manager oversight required

**Example:** Content creation with review (Research → Draft → Review → Revise)

## Memory and Context Management

### 1. Enable Memory for Long Conversations
```python
crew = Crew(
    agents=agents,
    tasks=tasks,
    memory=True,  # Maintain context across sessions
    embedder={"provider": "openai"}
)
```

### 2. Use Context Dependencies Wisely
- Only include necessary context
- Avoid circular dependencies
- Document data flow clearly

### 3. Shared State Patterns
Use context to pass state between tasks:

```yaml
task1:
  description: Generate analysis
  output_file: output/analysis.json

task2:
  description: Use analysis to generate recommendations
  context:
    - task1
```

## Tool Selection

### 1. Match Tools to Agent Role
```yaml
researcher:
  role: Research Specialist
  tools:
    - web_search
    - document_reader
    - calculator

writer:
  role: Content Writer
  tools:
    - grammar_checker
    - plagiarism_detector
```

### 2. Tool Quantity Guidelines
- **Minimum**: 0 (some agents work fine without tools)
- **Optimal**: 1-3 relevant tools
- **Maximum**: 5 (too many causes confusion)

### 3. Custom Tool Design
When building custom tools:
- Clear, specific names
- Well-documented descriptions
- Proper error handling
- Return structured data

## Error Handling

### 1. Retry Configuration
```yaml
agent:
  max_retry_limit: 3
  max_iterations: 25
```

### 2. Timeout Settings
```yaml
task:
  timeout: 600  # 10 minutes max
```

### 3. Fallback Strategies
```python
# Use try-except in callbacks
def safe_callback(result):
    try:
        process_result(result)
    except Exception as e:
        log_error(e)
        return default_result
```

## Performance Optimization

### 1. Rate Limiting
```python
crew = Crew(
    max_rpm=10,  # Prevent API throttling
    agents=agents,
    tasks=tasks
)
```

### 2. Caching
Enable caching to reduce API costs:
```python
crew = Crew(
    cache=True,
    agents=agents,
    tasks=tasks
)
```

### 3. Async Execution
Use async for independent tasks:
```yaml
async_task:
  async_mode: true
  max_workers: 5
```

### 4. LLM Selection
- Use smaller models for simple tasks
- Reserve GPT-4/Claude-3 for complex reasoning
- Consider cost vs. quality trade-offs

## Security Best Practices

### 1. API Key Management
- Use environment variables
- Never commit keys to version control
- Rotate keys regularly

### 2. Output Sanitization
```yaml
guardrails:
  - Do not output PII
  - Mask sensitive data
  - Validate JSON outputs
```

### 3. Tool Safety
Review custom tools for:
- Command injection vulnerabilities
- File system access limits
- Network security

## Testing and Validation

### 1. Use Validation Scripts
Always validate before running:
```bash
python scripts/validate_crew.py
```

### 2. Unit Test Tasks
Test individual tasks in isolation:
```python
def test_research_task():
    result = research_task.execute(inputs={"topic": "AI"})
    assert len(result) > 0
    assert "sources" in result
```

### 3. Integration Testing
Test complete workflows:
```python
def test_full_crew():
    result = crew.kickoff(inputs={"topic": "AI"})
    assert result is not None
    assert len(result.raw) > 100
```

## Common Anti-Patterns

### 1. Overlapping Agent Roles
❌ Bad: Multiple agents with similar roles competing
✅ Good: Clear role separation and specialization

### 2. Ambiguous Task Descriptions
❌ Bad: "Do some research"
✅ Good: "Find 5 recent papers on topic X with abstracts and key findings"

### 3. Missing Context Dependencies
❌ Bad: Task assumes data exists without declaring dependency
✅ Good: Explicit context dependencies documented

### 4. Over-complexity
❌ Bad: 20 agents for a simple task
✅ Good: Minimal agents needed to accomplish goal

### 5. Ignoring Expected Output
❌ Bad: Vague expected_output
✅ Good: Detailed, measurable completion criteria

## Version Control

### 1. Crew Configuration
- Store YAML configs in version control
- Use descriptive commit messages
- Tag stable versions

### 2. Prompt Management
- Track prompt versions
- Document prompt changes
- A/B test prompt variations

## Monitoring and Observability

### 1. Execution Logging
```python
crew = Crew(
    output_log_file="logs/crew.log",
    verbose=2
)
```

### 2. Token Usage Tracking
```python
result = crew.kickoff()
print(f"Tokens used: {result.token_usage}")
```

### 3. Performance Metrics
- Track execution time
- Monitor success rates
- Measure output quality
