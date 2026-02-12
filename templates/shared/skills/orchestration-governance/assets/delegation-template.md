# Delegation Template (Natural Language Edition)

Use this template as a guide for writing natural language instructions to specialists.

---

## Instruction Structure

When delegating work, include these elements in natural language:

### Required Elements

1. **Specialist to Ask**
   - Which specialist should do the work (builder, auditor, flow, docs)

2. **Action to Perform**
   - What specific action they should take
    - Use clear verbs: create, debug, transform, write, analyze, optimize

3. **Context and Requirements**
   - Relevant information gathered during questioning
   - File paths, component names, or locations
   - Tools or resources to use
   - Constraints or limitations

4. **Deliverables**
   - What outputs are expected
   - File formats and locations
   - Specific content requirements

### Optional Elements

5. **Success Criteria** (if specific)
   - How to know the task is complete
   - Quality standards to meet

6. **Dependencies** (if applicable)
   - What must be done first
   - What this task depends on

---

## Template Format

```
Ask the [specialist] to [action verb] [what]. 

Context:
- [Requirement 1]
- [Requirement 2]
- [File path or location]
- [Tool to use]
- [Constraint or preference]

Deliverables:
- [Output 1 with format and location]
- [Output 2 with format and location]

[Optional: Success criteria or dependencies]
```

---

## Example 1: Creating an Agent

**User Request:** "Create a web search agent"

**Natural Language Instruction:**

> Ask the builder to create a web research agent.
> 
> Context:
> - Agent name: "web_researcher"
> - Purpose: Research topics and summarize findings
> - Should use the web search tool
> - Target file: src/agents/web_researcher.yaml
> - Keep prompts concise and clear
> 
> Deliverables:
> - YAML configuration file at src/agents/web_researcher.yaml
> - Include role description, goal statement, and backstory
> - Define expected output format for the agent's responses
> - Use YAML-first approach

---

## Example 2: Debugging

**User Request:** "Fix the error in my crew"

**Natural Language Instruction:**

> Ask the auditor specialist to investigate the crew initialization error in read-only mode.
> 
> Context:
> - Error: ImportError when importing the crew
> - Location: src/my_crew/crew.py
> - Started after adding a new agent yesterday
> - Python version: 3.11
> 
> Deliverables:
> - Root cause analysis of the ImportError
> - Risk assessment and recommended fix options
> - Validation steps for confirming the recommended fix
>
> After auditor returns recommendations, ask the builder to implement the approved fix.

---

## Example 3: Architecture Transformation

**User Request:** "Convert my crew to use flows"

**Natural Language Instruction:**

> Ask the flow specialist to transform the existing crew to flow architecture.
> 
> Context:
> - Current crew uses traditional process-based approach
> - Crew location: src/my_crew/
> - 3 agents: researcher, analyst, writer
> - Want to use @start and @listen decorators
> - Maintain existing agent roles and goals
> 
> Deliverables:
> - Refactored crew using flow architecture
> - Flow implementation with proper routing
> - Updated documentation explaining the new structure
> - Transformation guide showing what changed

---

## Example 4: Documentation

**User Request:** "Write documentation"

**Natural Language Instruction:**

> Ask the docs specialist to create comprehensive documentation.
> 
> Context:
> - Project type: CrewAI application with 3 agents
> - Target audience: New developers joining the project
> - Should include setup and usage instructions
> - Use clear, professional language
> 
> Deliverables:
> - README.md with project overview
> - Setup instructions (step-by-step)
> - Usage examples with sample inputs/outputs
> - Architecture diagram (ASCII or markdown)

---

## Quick Reference: Phrasing by Specialist

### Builder
- "Ask the builder to create..."
- "Ask the builder to scaffold..."
- "Ask the builder to configure..."
- "Ask the builder to set up..."

### Auditor
- "Ask the auditor specialist to investigate..."
- "Ask the auditor specialist to audit..."
- "Ask the auditor specialist to validate..."
- "Ask the auditor specialist to trace root cause..."

### Flow
- "Ask the flow specialist to transform..."
- "Ask the flow specialist to refactor..."
- "Ask the flow specialist to design..."
- "Ask the flow specialist to orchestrate..."

### Docs
- "Ask the docs specialist to write..."
- "Ask the docs specialist to document..."
- "Ask the docs specialist to create..."
- "Ask the docs specialist to explain..."

---

## Tips for Clear Instructions

### Be Specific
> **Good:** "Ask the builder to create a YAML file at `src/agents/researcher.yaml`"
> **Bad:** "Ask the builder to make an agent file"

### Include All Context
> **Good:** "Configure it to use the web search tool with rate limiting of 10 requests per minute"
> **Bad:** "Make it use the web tool"

### State Constraints
> **Good:** "Keep all prompts under 200 tokens and use British English"
> **Bad:** "Write good prompts"

### Define Outputs Clearly
> **Good:** "Generate a markdown table listing all agents, their roles, and which tools they use"
> **Bad:** "Document the agents"
