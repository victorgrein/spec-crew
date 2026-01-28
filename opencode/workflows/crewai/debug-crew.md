# Debug Crew Workflow

## Overview

Workflow for debugging CrewAI execution issues.

## Trigger

- `/crew debug {crew_path} --trace="{trace_id}"`
- `/crew trace {crew_path} --task="{task_id}"`
- `/crew fix {crew_path} --issue="{description}"`
- "debug this crew", "fix this error", "why is this failing"

## Context Dependencies

- `context/crewai/processes/debugging.md`
- `context/crewai/domain/concepts/crews.md`
- `context/crewai/domain/concepts/agents.md`
- `context/crewai/domain/concepts/tasks.md`
- `context/crewai/standards/code-quality.md`

## Workflow Stages

### Stage 1: Gather Information

**Action:** Collect debugging information

**Subagent:** @debugger

**Process:**
1. Read crew/flow code
2. Identify error message or unexpected behavior
3. Check for trace ID or logs
4. Review recent changes
5. Identify affected components

**Output:** Issue summary with context

### Stage 2: Reproduce Issue

**Action:** Understand and reproduce the issue

**Process:**
1. Analyze execution flow
2. Identify where failure occurs
3. Check if issue is consistent or intermittent
4. Isolate the problematic component

**Output:** Reproduction steps and isolation

### Stage 3: Analyze Root Cause

**Action:** Identify root cause

**Subagent:** @debugger

**Process:**
1. Match symptoms to known issue patterns
2. Check configuration settings
3. Review agent/task definitions
4. Examine tool implementations
5. Analyze token usage and API calls

**Common Issues:**
- Rate limit errors → max_rpm configuration
- Context window exceeded → respect_context_window
- Tool not working → tool assignment, descriptions
- Agent loops → task clarity, max_iter
- Output parsing → Pydantic model, expected_output

**Output:** Root cause identification

### Stage 4: Implement Fix

**Action:** Create and apply fix

**Subagent:** @debugger, @coder-agent

**Process:**
1. Design fix based on root cause
2. Generate corrected code
3. Explain the fix
4. Ask user permission to apply

**Output:** Fix with explanation

### Stage 5: Verify Fix

**Action:** Verify the fix resolves the issue

**Process:**
1. Suggest verification steps
2. Recommend test inputs
3. Provide monitoring guidance
4. Suggest preventive measures

**Output:** Verification plan

## Success Criteria

- [ ] Issue clearly identified
- [ ] Root cause determined
- [ ] Fix addresses root cause
- [ ] Fix doesn't introduce new issues
- [ ] Verification steps provided
- [ ] Preventive measures suggested

## Output Format

```
## Debug Report

### Issue Summary
**Error**: {error_message}
**Component**: {agent|task|tool|flow}
**Severity**: {critical|high|medium|low}

### Root Cause
{detailed_analysis}

### Execution Trace
```
{execution_path}
```

### Fix
```python
# Before
{original_code}

# After
{fixed_code}
```

### Explanation
{why_this_fixes_the_issue}

### Verification Steps
1. {step_1}
2. {step_2}
3. {step_3}

### Preventive Measures
{recommendations}

**Apply this fix? [y/n]**
```

## Common Fixes

### Rate Limits
```python
agent = Agent(max_rpm=30)
```

### Context Window
```python
agent = Agent(respect_context_window=True)
```

### Tool Issues
```python
agent = Agent(tools=[MyTool()])  # Instantiate!
```

### Agent Loops
```python
agent = Agent(max_iter=15, allow_delegation=False)
```
