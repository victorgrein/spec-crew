# Custom Tool Playbook

## Goal

Define custom CrewAI tools with clear contracts, deterministic behavior, and production validation while keeping all planning examples in YAML agent/task format.

## Implementation Workflow

1. Define contract and gap.
   - Capture capability gap from built-in-tool analysis.
   - Define required inputs, output shape, and failure behavior.
2. Choose implementation path.
   - Select decorator style for small stateless transforms.
   - Select BaseTool style for integrations with env vars and dependencies.
3. Plan implementation artifacts.
   - Define schema fields and validation rules.
   - Define credentials, dependency list, retry policy, and timeout policy.
4. Plan verification.
   - Define test scenarios for missing env vars, invalid input, provider failures, and success path format.
5. Plan integration.
   - Define which agent uses the tool and when the tool is allowed to execute.

## BaseTool and Decorator Standards

- Ensure tool naming is explicit and action-oriented.
- Ensure schema fields are documented with clear descriptions.
- Ensure credential requirements are defined before runtime.
- Ensure output stays compact and parseable by downstream tasks.
- Ensure async policy is explicit for I/O-heavy providers.
- Ensure caching policy is explicit when deterministic reuse is safe.

## YAML Agent Example

```yaml
# agents.yaml
tool_architect_agent:
  role: CrewAI Tool Architect
  goal: Produce production-safe custom tool specifications from capability gaps.
  backstory: Specialist in args_schema design, env var policy, and provider integration quality.
  verbose: true
  tools:
    - FileReadTool
    - DirectoryReadTool

tool_validation_agent:
  role: Tool Validation Analyst
  goal: Validate custom tool plans against reliability, security, and testability gates.
  backstory: Focused on deterministic outputs and failure-safe execution.
  verbose: true
  tools:
    - FileReadTool
```

## YAML Task Example: Contract and Build Plan

```yaml
# tasks.yaml
custom_tool_contract_task:
  description: >
    Define a custom tool contract with explicit input schema,
    output contract, and error taxonomy.
    Include a decision note for BaseTool or decorator style.
  expected_output: >
    YAML specification with fields, constraints, failure codes,
    and implementation-style decision.
  agent: tool_architect_agent

custom_tool_build_plan_task:
  description: >
    Create an implementation plan covering env vars,
    package dependencies, timeout policy, retry policy,
    and cache policy.
  expected_output: >
    Ordered build checklist with acceptance criteria per step.
  agent: tool_architect_agent
  context:
    - custom_tool_contract_task
```

## YAML Task Example: Validation and Testing

```yaml
# tasks.yaml
custom_tool_test_matrix_task:
  description: >
    Define test scenarios for missing credentials,
    invalid schema inputs, upstream provider failures,
    timeout handling, and valid success responses.
  expected_output: >
    Test matrix with scenario name, input fixture,
    expected result, and pass/fail criteria.
  agent: tool_validation_agent
  context:
    - custom_tool_build_plan_task

custom_tool_release_readiness_task:
  description: >
    Validate release readiness by checking naming,
    schema completeness, env vars, dependency notes,
    observability notes, and rollback plan.
  expected_output: >
    Release checklist marked pass/fail with remediation notes.
  agent: tool_validation_agent
  context:
    - custom_tool_test_matrix_task
```

## YAML Task Example: Runtime Integration

```yaml
# tasks.yaml
tool_integration_policy_task:
  description: >
    Define which agent can call the custom tool,
    call limits, fallback behavior to built-in tools,
    and escalation rules when provider errors persist.
  expected_output: >
    Runtime policy document with allowed callers,
    max usage constraints, and fallback sequence.
  agent: tool_architect_agent
  context:
    - custom_tool_release_readiness_task
```

## Contribution-Level Checklist

- Classify capability gap and justify custom tool necessity.
- Define schema and validation rules before implementation.
- Define env vars and dependency requirements explicitly.
- Define deterministic output contract and error contract.
- Define test matrix for failure and success paths.
- Define runtime integration policy and fallback plan.
