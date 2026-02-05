---
name: crewai-llms
description: This skill should be used when user asks to "configure LLM", adjust "LLM settings", perform "model selection", set "rate limiting", tune a "context window", or optimize provider strategy for cost, latency, and quality. It provides guidance for selecting model tiers by task type, defining fallback behavior, and applying measurable optimization loops with clear targets. Use it when outputs are unstable, spend is rising, throughput is constrained, or context overflow causes truncation. It helps establish durable model policies and operational guardrails for reliable CrewAI execution at scale.
version: 1.0.0
---

# CrewAI LLMs

## What This Skill Does

Define a practical operating model for model configuration, provider selection, and performance tradeoff tuning in CrewAI implementations.
Organize decisions, guardrails, and review criteria so teams produce consistent provider settings, model choices, rate-limit policies, and optimization baselines.
Reduce rework by separating fast core guidance from deeper reference and example materials.

## When to Use This Skill

- Use this skill when work requires "configure LLM" outcomes with repeatable delivery quality.
- Use this skill when work requires "LLM settings" outcomes with repeatable delivery quality.
- Use this skill when work requires "model selection" outcomes with repeatable delivery quality.
- Use this skill when work requires "rate limiting" outcomes with repeatable delivery quality.
- Use this skill when work requires "context window" outcomes with repeatable delivery quality.
- Use this skill when work requires "provider configuration" outcomes with repeatable delivery quality.
- Use this skill when existing behavior is inconsistent and stronger operational standards are needed.
- Use this skill when implementation choices require explicit tradeoffs and documented decision rules.

## Key Concepts

- **Provider Strategy**: Choose providers based on capability, compliance needs, and operational stability.
- **Model Fit**: Map task class to model strengths before introducing advanced tuning.
- **Cost Target**: Set explicit spending targets and enforce them through model tiering.
- **Latency Target**: Define response-time objectives and tune model and process accordingly.
- **Quality Target**: Establish output quality criteria before measuring optimization success.
- **Function Calling LLM**: Use lower-cost models for tool-calling when semantic burden is light.
- **Rate Policy**: Apply request limits to avoid throttling failures and cascading retries.
- **Context Policy**: Manage context windows through summarization, chunking, and strict budgets.
- **Fallback Plan**: Define fallback models for outages and quota exhaustion events.
- **Measurement Loop**: Track usage metrics continuously and iterate based on observed outcomes.

## Quick Start

1. Define the immediate objective and the final acceptance criteria before writing configuration details.
2. Capture scope boundaries for model configuration, provider selection, and performance tradeoff tuning and record assumptions that affect downstream decisions.
3. Select the smallest viable implementation path that can be validated in one short feedback loop.
4. Reuse stable patterns from references before introducing any custom structure or novel behavior.
5. Document dependencies and interfaces so adjacent skills can consume outputs without ambiguity.
6. Validate expected outputs early to catch contract defects before broader orchestration begins.
7. Add observability points for key transitions, failures, and performance-sensitive operations.
8. Execute one representative run and compare outcomes against explicit acceptance criteria.
9. Resolve the highest-impact gaps first, then rerun the same scenario to verify improvement.
10. Promote the pattern to reusable guidance only after repeatable success across realistic inputs.
11. Link implementation artifacts to references and examples to preserve progressive disclosure.
12. Record follow-up actions for optimization, hardening, and documentation synchronization.

## Operational Notes

- Prioritize outcome clarity over implementation detail when initiating crewai-llms workstreams.
- Keep each decision reversible until validation confirms durability under realistic conditions.
- Isolate one variable per iteration when diagnosing quality, latency, or reliability regressions.
- Preserve naming consistency so logs, references, and handoffs remain easy to trace.
- Treat missing acceptance criteria as a blocking issue rather than an optional cleanup task.
- Align constraints, defaults, and fallback behavior before scaling execution volume.
- Use short review cycles to reduce expensive late-stage redesign and repeated retesting.
- Capture rationale for non-default choices so future maintainers can assess tradeoffs quickly.
- Keep externally visible outputs stable by validating format expectations before release.
- Prefer explicit interfaces between phases to avoid hidden coupling and fragile assumptions.
- Apply conservative limits first, then relax limits only with evidence from measured outcomes.
- Build reliability through deterministic workflows before adding advanced optimization layers.
- Track operational metrics continuously and escalate anomalies with context-rich reports.
- Enforce concise scopes for each run to protect budget, latency, and debugging speed.
- Review old guidance regularly and retire patterns that no longer match current behavior.

## Collaboration Boundaries

- Coordinate with related skills early when outputs from one phase become inputs to another phase.
- Define ownership for each artifact so review loops have clear accountability and completion signals.
- Avoid duplicating deep reference content inside SKILL.md and keep progressive disclosure strict.
- Share only essential context in cross-skill handoffs to protect focus and reduce token overhead.
- Escalate unresolved ambiguity as explicit decisions instead of embedding hidden assumptions.
- Reconcile terminology across skills to prevent mismatched interpretations during implementation.
- Validate interface compatibility whenever file structure, schema, or process sequencing changes.
- Record integration risks and mitigation steps before merging significant workflow changes.

## Detailed Operating Guidance

- Define a clear input contract before execution so upstream producers and downstream consumers interpret scope consistently.
- Establish quality thresholds for completeness, factuality, and formatting before tuning speed or cost-related parameters.
- Separate planning concerns from execution concerns so revisions do not unintentionally alter stable interface behavior.
- Keep assumption logs for uncertain requirements and convert unresolved assumptions into explicit decisions during review.
- Use bounded iterations with checkpoint reviews to prevent over-optimization that erodes maintainability and traceability.
- Prioritize deterministic outputs for automation-facing steps, then add expressive flexibility only where stakeholder value increases.
- Align naming and structural conventions with adjacent skills so handoffs remain understandable without extra translation work.
- Validate failure handling paths with representative bad inputs rather than relying only on happy-path testing.
- Capture performance observations in concise notes to support future optimization decisions with historical context.
- Treat every external dependency as potentially unreliable and design graceful fallback behavior from the start.
- Consolidate duplicate guidance into references to preserve one source of truth and reduce synchronization overhead.
- Tighten scope immediately when execution noise appears, then widen scope only after signal quality improves.
- Preserve auditability by linking key decisions to affected artifacts and expected operational outcomes.
- Prefer simple coordination mechanisms first, and expand orchestration complexity only when measurable benefit appears.
- Re-validate links, file names, and assumptions after structural refactors to avoid hidden documentation drift.

## Review Questions

- Which acceptance criterion provides the strongest signal that this implementation is ready for production use?
- Which assumption, if incorrect, would create the largest risk to correctness or downstream compatibility?
- Which part of the workflow has the least observability and therefore needs better trace instrumentation?
- Which configuration choice offers the best cost-quality balance for the current delivery objective?
- Which dependency could fail silently, and what detection mechanism would expose that failure quickly?
- Which output field or artifact format is most likely to break consumer integrations after changes?
- Which retry or fallback strategy is missing for the highest-latency or least-reliable operation?
- Which section of guidance can be simplified without losing decision quality or implementation safety?
- Which unresolved ambiguity should be escalated before the next implementation iteration begins?
- Which evidence confirms that recent edits improved outcomes instead of merely changing behavior?

## Quality Signals

- Validate outcomes against explicit acceptance criteria and operational constraints before promoting guidance to reusable standards.
- Compare a baseline run and a revised run to confirm improvements in reliability, latency, or cost without hidden regressions.
- Record rationale for every non-default decision so maintainers can audit tradeoffs quickly during future updates.

## Validation Checklist

- [ ] Confirm frontmatter uses only `name`, `description`, and `version` fields.
- [ ] Confirm body guidance stays concise, actionable, and focused on operational decisions.
- [ ] Confirm language remains imperative or infinitive and avoids second-person directives.
- [ ] Confirm no tables are present in SKILL.md and move tabular detail to references.
- [ ] Confirm no code blocks are present in SKILL.md and move runnable content to examples.
- [ ] Confirm scope statements align with the intended model configuration, provider selection, and performance tradeoff tuning objective.
- [ ] Confirm trigger scenarios remain specific enough to activate the correct skill reliably.
- [ ] Confirm key concepts define stable vocabulary used consistently across related files.
- [ ] Confirm quick-start steps form a complete path from planning through validation.
- [ ] Confirm decision rationale exists for non-default settings and unusual execution paths.
- [ ] Confirm operational limits and safeguards are explicit for high-cost or high-risk actions.
- [ ] Confirm logging and trace requirements are sufficient for efficient incident diagnosis.
- [ ] Confirm acceptance criteria are measurable and tied to expected output contracts.
- [ ] Confirm cross-skill dependencies are named and linked to concrete resource files.
- [ ] Confirm references contain deep technical detail and examples contain runnable artifacts.
- [ ] Confirm guidance remains current with project structure and naming conventions.
- [ ] Confirm ambiguity is reduced by replacing vague language with explicit decision rules.
- [ ] Confirm failure modes and fallback behavior are addressed at least at a high level.
- [ ] Confirm final review checks readability, correctness, and maintainability standards.
- [ ] Confirm links in Additional Resources resolve correctly from this skill directory.

## Common Mistakes to Avoid

- Avoid combining multiple unrelated objectives into one run without explicit decomposition.
- Avoid vague completion definitions that force subjective reviews and repeated rework cycles.
- Avoid adding advanced options before validating a stable baseline behavior path.
- Avoid relying on defaults that were not reviewed against current project constraints.
- Avoid pushing deep implementation detail into SKILL.md where discoverability should stay high.
- Avoid silent handoff assumptions when dependencies cross skills or ownership boundaries.
- Avoid changing structure and behavior simultaneously when debugging active regressions.
- Avoid skipping post-change verification, even when edits appear small and localized.
- Avoid stale links to renamed files after directory or filename standardization work.
- Avoid retaining obsolete guidance that conflicts with current references and examples.

## Additional Resources

For detailed documentation and examples:
- **[Complete Reference](references/complete-reference.md)** - Full API details, options, and extended guidance.
- **[Patterns Guide](references/patterns-reference.md)** - Reusable archetypes, workflows, and decision patterns.
- **[Basic Setup](examples/basic-setup.md)** - Minimal starting path for first implementation pass.
- **[Code Examples](examples/python-code.md)** - Runnable Python-oriented implementation patterns.
- **[YAML Configs](examples/yaml-config.md)** - Declarative configuration examples and templates.
