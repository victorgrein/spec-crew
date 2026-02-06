---
name: tools
description: Consolidated skill pack for CrewAI tool selection, custom tool development, and safe integration patterns.
version: 1.0.0
---

# Tools

## What This Pack Covers

Tooling guidance for robust CrewAI integration and operational safety.

- Built-in tool selection
- Custom `BaseTool` design
- Argument contracts and validation
- Timeout, retries, async paths, and caching

## Use This Pack When

- The request asks to create or refactor tools.
- Tool failures or reliability issues affect runtime behavior.
- The user needs safer external integrations.

## Normalized Trigger Phrases

- create custom tool
- tool integration
- tool timeout
- tool caching
- tool schema
- async tool

## Operating Rules

- Keep tool contracts explicit and minimal.
- Validate arguments before side effects.
- Prefer built-in tools when they satisfy requirements.

## Additional Resources

- `references/index.md`
- `examples/index.md`
