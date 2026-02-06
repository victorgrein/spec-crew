---
description: Canonical command for debugging and optimization changes
agent: crewai-orchestrator
canonical: true
command_id: crew.fix.v1
---

# /crew fix

Canonical command for resolving failures and applying runtime optimizations.

## Syntax

```
/crew fix {crew_path} [--trace="{trace_id}"] [--target="{stability|cost|latency|quality}"]
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| crew_path | Yes | Path to the crew or flow to fix |
| --trace | No | Optional trace identifier for failure analysis |
| --target | No | Optimization focus (default: `stability`) |

## What It Does

1. Diagnoses execution issues and root causes
2. Reviews configuration for performance and cost opportunities
3. Proposes or applies targeted fixes with rationale
4. Returns deterministic validation steps

## Output

- Root-cause findings
- Fix and optimization plan
- Concrete code/config changes
- Post-fix verification checklist

## Response Contract (Required)

Every command response must include these sections in order:

1. `findings` - observations grounded in repository evidence
2. `plan` - ordered execution steps
3. `proposed changes` - concrete file/config changes (or `none`)
4. `validation steps` - checks to confirm correctness

## Related Commands

- `/crew inspect` - Diagnose before changing
- `/crew evolve` - Perform broader structural refactors
- `/crew docs` - Document fixes and operational guidance
