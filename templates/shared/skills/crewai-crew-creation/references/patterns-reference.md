# CrewAI Crew Creation - Patterns and Archetypes

This document captures reusable patterns, archetypes, and workflow guidance for `crewai-crew-creation`.

## Common Archetypes and Patterns

### Creation Process

1. Define the Goal
2. Identify Required Agents
3. Design Tasks
4. Choose Process Type
5. Create Project Structure
6. Configure Agents (YAML)
7. Configure Tasks (YAML)
8. Implement Crew Class
9. Test the Crew
10. Iterate and Refine

### Process Steps

- Refer to SKILL.md for details.

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

### Validation Checklist

- [ ] All agents have clear roles, goals, backstories
- [ ] All tasks have clear descriptions and expected outputs
- [ ] Task dependencies are correctly defined
- [ ] Tools are assigned to appropriate agents
- [ ] Process type matches workflow complexity
- [ ] Verbose mode enabled for debugging
- [ ] Output files specified where needed
- [ ] Environment variables configured

### Common Issues

| Issue | Solution |
|-------|----------|
| Agent not using tools | Check tool assignment, improve tool descriptions |
| Task output unclear | Make expected_output more specific |
| Context not passing | Verify context list in task definition |
| Rate limits | Add max_rpm to agents or crew |
| Long execution | Enable caching, reduce max_iter |

## Integration Patterns

- Pair with `crewai-agents` for role/goal/backstory contracts.
- Pair with `crewai-tasks` for deterministic output and dependencies.
- Pair with `crewai-debugging` and `crewai-optimization` for reliability/performance loops.

## Workflow Notes

- Define constraints first, then implementation details.
- Use measurable checkpoints at each major step.
- Preserve progressive disclosure: keep SKILL.md concise and place depth here.
