# CrewAI Optimization - Complete Reference

This document centralizes detailed reference material for `crewai-optimization` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `optimization-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Optimization Targets
-   Model Selection Guide
- Optimization Process
-   Step 1: Baseline Measurement
-   Step 2: Identify Bottlenecks
-   Step 3: Apply Optimizations
-   Step 4: Measure Improvement
-   Step 5: Iterate
- Cost Optimization
-   Tiered Model Strategy
- Latency Optimization
-   Parallel Execution
- Quality Optimization
-   Add Review Task
- Cost Estimation
- Optimization Checklist
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Target | Focus | Key Strategies |
|--------|-------|----------------|
| Cost | Reduce API costs | Cheaper models, caching, reduce iterations |
| Latency | Reduce execution time | Fast models, async, caching |
| Quality | Maximize output quality | Best models, reasoning, memory |

### Table 2

| Optimization | Main LLM | Function Calling LLM |
|--------------|----------|---------------------|
| Cost | gpt-4o-mini | gpt-3.5-turbo |
| Latency | gpt-4o-mini | gpt-4o-mini |
| Quality | gpt-4o | gpt-4o-mini |
| Balanced | gpt-4o-mini | gpt-3.5-turbo |

## Edge Cases and Limitations

- Validate configuration compatibility before execution.
- Keep prompts concise to avoid context-window pressure.
- Add retries and guardrails for external tool/API calls.

## Common Pitfalls

| Problem | Cause | Solution |
|---|---|---|
| Ambiguous outcomes | Expected outputs are underspecified | Define concrete acceptance criteria and output format. |
| Execution drift | Role/task boundaries are unclear | Tighten role, goal, and task contracts. |
| Rework loops | Validation occurs too late | Add checkpoints and early review tasks. |
| Tool instability | Missing error handling and retries | Implement timeouts, retries, and fallback behavior. |

## Additional Notes

- This file is generated for Phase 4 standardization and can be expanded with skill-specific deep dives in later iterations.
