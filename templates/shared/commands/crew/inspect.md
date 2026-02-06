---
description: Canonical command for architecture and performance inspection
agent: crewai-orchestrator
canonical: true
command_id: crew.inspect.v1
---

# /crew inspect

Canonical command for analyzing architecture quality and runtime performance.

## Syntax

```
/crew inspect {crew_path} [--focus="{architecture|performance|full}"]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| crew_path | Yes | Path to a CrewAI crew or flow |
| --focus | No | Inspection mode (default: `full`) |

## What It Does

1. Reads crew and flow configuration
2. Evaluates architecture quality and ownership boundaries
3. Reviews LLM, task, and process settings for bottlenecks
4. Produces prioritized recommendations with severity

## Output

- Architecture and runtime findings
- Risk and bottleneck summary
- Ordered remediation plan
- Verification checklist

## Response Contract (Required)

Every command response must include these sections in order:

1. `findings` - observations grounded in repository evidence
2. `plan` - ordered execution steps
3. `proposed changes` - concrete file/config changes (or `none`)
4. `validation steps` - checks to confirm correctness

## Related Commands

- `/crew init` - Initialize or bootstrap project scaffolding
- `/crew fix` - Apply fixes for detected issues
- `/crew docs` - Generate updated technical documentation
