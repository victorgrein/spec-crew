# CrewAI Crew Creation - Complete Reference

This document centralizes detailed reference material for `crewai-crew-creation` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `crew-creation-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Creation Process
- Process Steps
-   Step 1: Define the Goal
-   Step 2: Identify Required Agents
-   Step 3: Design Tasks
-   Step 4: Choose Process Type
-   Step 5: Create Project Structure
-   Step 6: Configure Agents (YAML)
-   Step 7: Configure Tasks (YAML)
-   Step 8: Implement Crew Class
-   Step 9: Test the Crew
-   Step 10: Iterate and Refine
- Validation Checklist
- Common Issues
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Issue | Solution |
|-------|----------|
| Agent not using tools | Check tool assignment, improve tool descriptions |
| Task output unclear | Make expected_output more specific |
| Context not passing | Verify context list in task definition |
| Rate limits | Add max_rpm to agents or crew |
| Long execution | Enable caching, reduce max_iter |

## Edge Cases and Limitations

- Review `Common Issues` in `../SKILL.md` during troubleshooting.

## Common Pitfalls

| Problem | Cause | Solution |
|---|---|---|
| Ambiguous outcomes | Expected outputs are underspecified | Define concrete acceptance criteria and output format. |
| Execution drift | Role/task boundaries are unclear | Tighten role, goal, and task contracts. |
| Rework loops | Validation occurs too late | Add checkpoints and early review tasks. |
| Tool instability | Missing error handling and retries | Implement timeouts, retries, and fallback behavior. |

## Additional Notes

- This file is generated for Phase 4 standardization and can be expanded with skill-specific deep dives in later iterations.
