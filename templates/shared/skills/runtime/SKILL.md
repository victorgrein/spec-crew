---
name: runtime
description: Consolidated skill pack for CrewAI runtime operations, including debugging, optimization, LLM tuning, and memory behavior.
version: 1.0.0
---

# Runtime

## What This Pack Covers

Runtime diagnosis and optimization guidance for stability, cost, latency, and quality.

- Trace and failure diagnosis
- Performance and bottleneck triage
- LLM model/tokens tuning
- Memory and context stability strategies

## Use This Pack When

- The request is rooted in `/crew inspect` or `/crew fix`.
- Execution failures, regressions, or timeouts are present.
- The user asks for measurable runtime optimization.

## Normalized Trigger Phrases

- debug crew
- trace failure
- optimize latency
- optimize token cost
- llm tuning
- memory stability

## Operating Rules

- Prioritize root-cause fixes before aggressive optimization.
- Tie every recommendation to evidence and a measurable outcome.
- Keep validation deterministic and reproducible.

## Additional Resources

- `references/index.md`
- `examples/index.md`
