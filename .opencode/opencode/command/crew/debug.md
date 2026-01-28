---
description: Debug CrewAI execution issues using traces
agent: crewai-orchestrator
---

# /crew debug

Debug CrewAI crew or flow execution issues by analyzing traces and identifying root causes.

## Syntax

```
/crew debug {crew_path} [--trace="{trace_id}"]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| crew_path | Yes | Path to the crew directory or file |
| --trace | No | Specific trace ID to analyze |

## Examples

```
/crew debug ./my_crew

/crew debug ./my_crew --trace="abc123"

/crew debug src/my_flow/main.py
```

## What It Does

1. **Reads** crew/flow code and configuration
2. **Analyzes** error messages or unexpected behavior
3. **Identifies** the failing component
4. **Determines** root cause
5. **Generates** fix with explanation
6. **Requests** permission to apply fix

## Common Issues Detected

| Issue | Symptoms | Fix |
|-------|----------|-----|
| Rate Limits | 429 errors | Add max_rpm |
| Context Window | Truncated output | Enable respect_context_window |
| Tool Errors | Tool not found | Check tool assignment |
| Agent Loops | max_iter reached | Clarify task, reduce iterations |
| Output Parsing | Pydantic errors | Fix expected_output format |

## Output

- Issue summary
- Root cause analysis
- Execution trace
- Fix with code
- Verification steps
- Preventive measures

## Related Commands

- `/crew trace` - Trace execution path
- `/crew fix` - Fix specific issue
- `/crew analyze` - Analyze performance
