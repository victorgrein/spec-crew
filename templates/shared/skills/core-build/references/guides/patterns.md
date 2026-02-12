# CrewAI Design Patterns

Common patterns for building effective CrewAI applications.

## Research → Analysis → Report Pattern

The most fundamental pattern for information processing workflows.

```yaml
# Agents
researcher:
  role: Research Specialist
  goal: Gather comprehensive information
  backstory: Expert at finding and organizing data

analyst:
  role: Data Analyst  
  goal: Extract insights and identify patterns
  backstory: Skilled at turning data into insights

report_writer:
  role: Report Writer
  goal: Create clear, actionable reports
  backstory: Expert at communicating complex information

# Tasks
research_task:
  description: >
    Research {topic} thoroughly.
    Find 10-15 key sources.
    Compile raw findings.
  expected_output: Raw research data with sources
  agent: researcher
  output_file: output/research.md

analysis_task:
  description: >
    Analyze research findings.
    Identify 5-7 key themes.
    Find patterns and insights.
  expected_output: Analysis with themes and insights
  agent: analyst
  context:
    - research_task
  output_file: output/analysis.md

report_task:
  description: >
    Write comprehensive report.
    Include executive summary.
    Provide actionable recommendations.
  expected_output: Polished report ready for stakeholders
  agent: report_writer
  context:
    - research_task
    - analysis_task
  output_file: output/final_report.md
```

**Use when:** Information synthesis, market research, competitive analysis

---

## Data Extraction → Validation → Storage Pattern

For ETL (Extract, Transform, Load) workflows.

```yaml
# Agents
extractor:
  role: Data Extraction Specialist
  goal: Extract data from sources accurately
  tools:
    - file_reader
    - web_scraper

validator:
  role: Data Quality Specialist
  goal: Ensure data accuracy and completeness

storer:
  role: Database Specialist
  goal: Store validated data properly

# Tasks
extraction_task:
  description: Extract data from {source}
  expected_output: Raw extracted data
  agent: extractor

validation_task:
  description: >
    Validate extracted data:
    - Check completeness
    - Verify data types
    - Identify anomalies
  expected_output: Validation report with issues
  agent: validator
  context:
    - extraction_task

storage_task:
  description: Store validated data in {destination}
  expected_output: Storage confirmation
  agent: storer
  context:
    - validation_task
```

**Use when:** Data pipelines, ETL processes, data migration

---

## Multi-Agent Collaboration Pattern

Specialized agents working together on different aspects.

```yaml
# Agents
frontend_dev:
  role: Frontend Developer
  goal: Build user interfaces
  tools:
    - code_writer
    - linter

backend_dev:
  role: Backend Developer
  goal: Build APIs and services
  tools:
    - code_writer
    - api_tester

tester:
  role: QA Engineer
  goal: Ensure quality and catch bugs
  tools:
    - test_runner
    - bug_tracker

# Tasks
frontend_task:
  description: Build UI components for {feature}
  expected_output: Frontend code
  agent: frontend_dev

backend_task:
  description: Build API endpoints for {feature}
  expected_output: Backend code
  agent: backend_dev

integration_task:
  description: >
    Test frontend and backend integration.
    Run integration tests.
    Report issues.
  expected_output: Test results
  agent: tester
  context:
    - frontend_task
    - backend_task
```

**Use when:** Software development, complex projects, domain-specific expertise

---

## Review Loop Pattern

Iterative improvement with feedback cycles.

```yaml
# Agents
creator:
  role: Content Creator
  goal: Produce initial drafts

reviewer:
  role: Senior Editor
  goal: Provide quality feedback

reviser:
  role: Content Reviser
  goal: Incorporate feedback effectively

# Tasks
draft_task:
  description: Create initial draft of {content}
  expected_output: First draft
  agent: creator

review_task:
  description: >
    Review draft and provide:
    - Strengths
    - Areas for improvement
    - Specific suggestions
  expected_output: Detailed feedback
  agent: reviewer
  context:
    - draft_task

revision_task:
  description: Revise content based on feedback
  expected_output: Improved draft
  agent: reviser
  context:
    - draft_task
    - review_task

final_review_task:
  description: Final quality check
  expected_output: Approved final version
  agent: reviewer
  context:
    - revision_task
```

**Use when:** Content creation, code review, quality assurance

---

## Decision Tree Pattern

Conditional execution based on task outcomes.

```yaml
# Agents
analyzer:
  role: Business Analyst
  goal: Assess situations and recommend paths

decision_maker:
  role: Decision Authority
  goal: Make final decisions

executor_a:
  role: Path A Specialist
  goal: Execute option A

executor_b:
  role: Path B Specialist
  goal: Execute option B

# Tasks
analysis_task:
  description: Analyze {situation} and identify options
  expected_output: Analysis with options
  agent: analyzer

decision_task:
  description: >
    Choose between options:
    - Option A: if condition X
    - Option B: if condition Y
    Provide decision with rationale
  expected_output: Decision document
  agent: decision_maker
  context:
    - analysis_task

# Conditional execution - use python logic
option_a_task:
  description: Execute option A approach
  expected_output: Results from option A
  agent: executor_a
  context:
    - decision_task

option_b_task:
  description: Execute option B approach
  expected_output: Results from option B
  agent: executor_b
  context:
    - decision_task
```

**Use when:** Conditional workflows, branching logic, approval processes

---

## Parallel Processing Pattern

Multiple independent tasks executing simultaneously.

```yaml
# Agents
processor_1:
  role: Data Processor A
  goal: Process section A

processor_2:
  role: Data Processor B
  goal: Process section B

processor_3:
  role: Data Processor C
  goal: Process section C

aggregator:
  role: Results Aggregator
  goal: Combine parallel results

# Tasks
task_a:
  description: Process data segment A
  expected_output: Results A
  agent: processor_1
  async_mode: true

task_b:
  description: Process data segment B
  expected_output: Results B
  agent: processor_2
  async_mode: true

task_c:
  description: Process data segment C
  expected_output: Results C
  agent: processor_3
  async_mode: true

aggregation_task:
  description: >
    Combine results from parallel tasks.
    Resolve any conflicts.
    Produce unified output.
  expected_output: Combined results
  agent: aggregator
  context:
    - task_a
    - task_b
    - task_c
```

**Use when:** Batch processing, data segmentation, performance optimization

---

## Hierarchical Management Pattern

Manager overseeing worker agents in structured process.

```python
from crewai import Agent, Crew, Process, Task

# Workers
researcher = Agent(role="Researcher", goal="Find information")
writer = Agent(role="Writer", goal="Create content")
editor = Agent(role="Editor", goal="Review content")

# Manager
manager = Agent(
    role="Project Manager",
    goal="Coordinate team and ensure quality",
    allow_delegation=True
)

# Tasks
tasks = [
    Task(description="Research topic", agent=researcher),
    Task(description="Write article", agent=writer),
    Task(description="Edit article", agent=editor)
]

# Hierarchical crew
crew = Crew(
    agents=[researcher, writer, editor, manager],
    tasks=tasks,
    process=Process.hierarchical,
    manager_agent=manager,
    verbose=True
)
```

**Use when:** Complex projects, quality oversight, team coordination

---

## Human-in-the-Loop Pattern

Pause for human review at critical points.

```yaml
# Agents
preparer:
  role: Report Preparer
  goal: Draft reports

reviewer:
  role: Content Reviewer
  goal: Ensure accuracy

finalizer:
  role: Document Finalizer
  goal: Produce final version

# Tasks
prepare_task:
  description: Prepare draft report
  expected_output: Draft document
  agent: preparer

review_task:
  description: Review and approve draft
  expected_output: Approved or rejected with feedback
  agent: reviewer
  context:
    - prepare_task
  human_input: true  # Pause for human review

finalize_task:
  description: Create final version
  expected_output: Final document
  agent: finalizer
  context:
    - review_task
```

**Use when:** Critical decisions, regulatory compliance, quality gates

---

## Orchestrator Pattern

Meta-agent coordinating multiple sub-crews.

```python
from crewai import Crew, Process

# Define sub-crews for different domains
research_crew = Crew(...)  # Research specialists
writing_crew = Crew(...)   # Content creators
design_crew = Crew(...)    # Visual designers

# Orchestrator crew coordinates them
orchestrator = Agent(
    role="Project Orchestrator",
    goal="Coordinate domain-specific crews",
    tools=[
        research_crew.as_tool(),
        writing_crew.as_tool(),
        design_crew.as_tool()
    ]
)
```

**Use when:** Large projects, multiple domains, complex coordination

## Pattern Selection Guide

| Pattern | Best For | Complexity |
|---------|----------|------------|
| Research → Analysis → Report | Information processing | Low |
| Data Extraction → Validation → Storage | Data pipelines | Medium |
| Multi-Agent Collaboration | Complex projects | Medium-High |
| Review Loop | Quality assurance | Medium |
| Decision Tree | Conditional workflows | Medium |
| Parallel Processing | Performance optimization | Medium |
| Hierarchical Management | Team coordination | High |
| Human-in-the-Loop | Critical approvals | Medium |
| Orchestrator | Large-scale projects | Very High |
