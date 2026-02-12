# Subagent Directory

## @builder
Purpose: build crews, agents, tasks, tools, and memory configuration.

- Allowed skills: `core-build`, `tools-expert`
- Use when: create, scaffold, setup, bootstrap, build

## @flow
Purpose: implement and refactor flow orchestration.

- Allowed skills: `flows` only
- Use when: flow, state-management, routing, orchestration, decorators

## @auditor
Purpose: run read-only investigations and audits.

- Allowed skills: `core-build`, `flows`, `tools-expert`
- Execution: read-only
- Output: findings, risk assessment, recommendations, validation steps

## @docs
Purpose: maintain project documentation.

- Allowed skills: `core-build`, `flows`
- Write policy: only `*.md`
- Bash policy: read-only commands only
