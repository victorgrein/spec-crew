# Crew Creation Process

## Overview

Step-by-step workflow for creating a new CrewAI crew from specification.

## Prerequisites

- CrewAI installed (`pip install crewai 'crewai[tools]'`)
- API keys configured (OPENAI_API_KEY, etc.)
- Clear understanding of the task to accomplish

## Process Steps

### Step 1: Define the Goal

**Questions to answer:**
- What is the crew's primary objective?
- What inputs will it receive?
- What outputs should it produce?
- What quality standards must it meet?

**Output:** Clear goal statement and success criteria

### Step 2: Identify Required Agents

**For each agent, define:**
- Role: What expertise does this agent have?
- Goal: What is this agent trying to achieve?
- Backstory: What context shapes this agent's behavior?
- Tools: What capabilities does this agent need?

**Common patterns:**
- Research → Analysis → Writing
- Data Collection → Processing → Reporting
- Planning → Execution → Review

### Step 3: Design Tasks

**For each task, define:**
- Description: Clear, specific instructions
- Expected Output: Measurable deliverable
- Agent: Who performs this task
- Context: Dependencies on other tasks
- Tools: Task-specific tools (optional)

**Task ordering:**
- List tasks in execution order
- Define context dependencies explicitly
- Consider async execution for independent tasks

### Step 4: Choose Process Type

**Sequential (Default):**
- Linear workflow
- Each task depends on previous
- Simple, predictable

**Hierarchical:**
- Manager coordinates workers
- Dynamic delegation
- Complex, interdependent tasks
- Requires `manager_llm` or `manager_agent`

### Step 5: Create Project Structure

```bash
crewai create crew my_crew
cd my_crew
```

**Edit configuration files:**
- `config/agents.yaml` - Agent definitions
- `config/tasks.yaml` - Task definitions
- `crew.py` - Crew class with decorators

### Step 6: Configure Agents (YAML)

```yaml
# config/agents.yaml
researcher:
  role: >
    {topic} Research Specialist
  goal: >
    Find comprehensive, accurate information about {topic}
  backstory: >
    Expert researcher with years of experience finding
    and synthesizing information from diverse sources.

writer:
  role: >
    Content Writer
  goal: >
    Create engaging, well-structured content
  backstory: >
    Skilled writer who transforms complex information
    into clear, compelling narratives.
```

### Step 7: Configure Tasks (YAML)

```yaml
# config/tasks.yaml
research_task:
  description: >
    Research {topic} thoroughly. Find key facts, recent
    developments, and expert opinions.
  expected_output: >
    Comprehensive research report with:
    - Key findings (5+ points)
    - Sources cited
    - Recent developments
  agent: researcher

writing_task:
  description: >
    Write an engaging article about {topic} based on
    the research findings.
  expected_output: >
    Well-structured article (800-1200 words) in markdown
    format with introduction, body, and conclusion.
  agent: writer
  context:
    - research_task
  output_file: output/article.md
```

### Step 8: Implement Crew Class

```python
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool

@CrewBase
class MyCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SerperDevTool()],
            verbose=True
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config['research_task'])

    @task
    def writing_task(self) -> Task:
        return Task(
            config=self.tasks_config['writing_task'],
            output_file='output/article.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
```

### Step 9: Test the Crew

```bash
# Install dependencies
crewai install

# Activate environment
source .venv/bin/activate

# Run with test input
crewai run
```

### Step 10: Iterate and Refine

**Common refinements:**
- Adjust agent backstories for better behavior
- Clarify task descriptions
- Add/remove tools
- Tune LLM settings
- Enable memory for complex tasks

## Validation Checklist

- [ ] All agents have clear roles, goals, backstories
- [ ] All tasks have clear descriptions and expected outputs
- [ ] Task dependencies are correctly defined
- [ ] Tools are assigned to appropriate agents
- [ ] Process type matches workflow complexity
- [ ] Verbose mode enabled for debugging
- [ ] Output files specified where needed
- [ ] Environment variables configured

## Common Issues

| Issue | Solution |
|-------|----------|
| Agent not using tools | Check tool assignment, improve tool descriptions |
| Task output unclear | Make expected_output more specific |
| Context not passing | Verify context list in task definition |
| Rate limits | Add max_rpm to agents or crew |
| Long execution | Enable caching, reduce max_iter |
