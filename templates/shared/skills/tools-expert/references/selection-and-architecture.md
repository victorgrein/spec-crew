# Tool Selection and Architecture

## Decision Algorithm

1. Define success contract.
   - Required inputs
   - Expected output shape
   - Latency and reliability requirements
   - Security and compliance constraints
2. Match built-in categories first.
   - Use `references/tools-landscape.md`
   - Confirm setup complexity and credential availability
3. Choose one path.
   - Built-in only
   - Hybrid (built-in plus one custom tool)
   - Fully custom (only when no acceptable built-in path exists)
4. Minimize tool surface area.
   - Assign only required tools to each agent
   - Cap high-frequency tools with `max_usage_count` when needed
5. Validate behavior under failure.
   - Missing credentials
   - API/network failures
   - Empty results
   - Invalid inputs

## Built-In vs Custom Matrix

| Condition | Preferred Path |
| --- | --- |
| Built-in tool already covers use case | Built-in only |
| Built-in covers 80% but output format is mismatched | Hybrid (adapter custom tool) |
| Vendor API is unsupported by built-ins | Custom `BaseTool` |
| Logic is a tiny deterministic transform | Custom `@tool` |
| Retrieval over domain-specific corpus | `RagTool` or retrieval adapter |
| Strict enterprise guardrails and observability required | Built-in/integration first, custom only for policy gaps |

## Custom Tool Style Matrix

| Requirement | `@tool` Decorator | `BaseTool` Subclass |
| --- | --- | --- |
| Stateless helper function | Best fit | Works but heavier |
| Configurable fields and defaults | Limited | Best fit |
| `args_schema` validation contract | Optional/simple | Strong fit |
| Env vars and dependency metadata | Weak | Strong (`env_vars`, `package_dependencies`) |
| Complex error handling/retries | Possible | Best fit |
| Reusable production integration | Usually no | Best fit |

## Architecture Patterns

### Pattern A: Specialist Pair

- Research agent: search/scraping tools
- Synthesis agent: file/database/code tools
- Benefit: keep each tool stack focused and predictable

### Pattern B: Retrieval Gateway

- Retrieval agent: RAG/document tools only
- Downstream agent: reasoning/writing without retrieval noise
- Benefit: isolate retrieval failures and simplify prompts

### Pattern C: Integration Handoff

- CrewAI agent: triage and decision
- Integration tool: invoke external automation or Bedrock agent
- Benefit: reuse existing production automations and guardrails

### Pattern D: Hybrid Adapter

- Built-in tool handles core retrieval/search
- One custom adapter normalizes output to strict schema
- Benefit: avoid rewriting mature integration logic

## Operational Guardrails

- Keep each agent under a small, role-aligned tool list
- Avoid multiple tools with overlapping semantics unless fallback is intentional
- Add clear task instructions for when each tool should be called
- Avoid placing write/destructive tools on agents that only need read access
- Enforce explicit timeout and retry behavior in custom tools

## Anti-Patterns

- Building custom wrappers for existing built-ins without a meaningful contract gap
- Combining unrelated API actions in one monolithic tool
- Returning verbose, unstructured payloads that bloat context
- Hiding required credentials until runtime failure deep in execution
- Treating custom tools as prompt workarounds instead of stable integrations

## Final Readiness Check

- Built-in options evaluated and documented
- Custom path justified with explicit capability gap
- `args_schema` and input validation complete
- Credential and dependency requirements declared
- Tests cover happy path and failure modes
- Tool output format validated against downstream consumer needs
