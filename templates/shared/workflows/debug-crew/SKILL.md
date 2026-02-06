---
name: debug-crew
description: Debug CrewAI execution issues by analyzing traces, identifying failures, and providing fixes. Use when encountering errors, failures, or unexpected behavior.
context: fork
agent: general-purpose
skills:
  - runtime
  - tools
---

# Debug Crew Workflow

Debug the CrewAI execution issue: $ARGUMENTS

## Your Process

### Stage 1: Gather Information
1. Read crew/flow code
2. Identify error message or unexpected behavior
3. Check for trace ID or logs
4. Review recent changes
5. Identify affected components

### Stage 2: Reproduce Issue
1. Analyze execution flow
2. Identify where failure occurs
3. Check if issue is consistent or intermittent
4. Isolate the problematic component

### Stage 3: Analyze Root Cause
Match symptoms to known issue patterns:

**Common Issues:**
- Rate limit errors → max_rpm configuration
- Context window exceeded → respect_context_window
- Tool not working → tool assignment, descriptions
- Agent loops → task clarity, max_iter
- Output parsing → Pydantic model, expected_output

### Stage 4: Implement Fix
1. Design fix based on root cause
2. Generate corrected code
3. Explain the fix
4. Ask user permission to apply

### Stage 5: Verify Fix
1. Suggest verification steps
2. Recommend test inputs
3. Provide monitoring guidance
4. Suggest preventive measures

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

## Common Fixes Reference

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

## Success Criteria
- [ ] Issue clearly identified
- [ ] Root cause determined
- [ ] Fix addresses root cause
- [ ] Fix doesn't introduce new issues
- [ ] Verification steps provided
- [ ] Preventive measures suggested
