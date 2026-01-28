# CrewAI Processes Navigation

## Overview

This directory contains step-by-step workflows for common CrewAI operations.

## Available Processes

| File | Description | When to Use |
|------|-------------|-------------|
| [crew-creation.md](crew-creation.md) | Create new crew from scratch | Starting new crew project |
| [debugging.md](debugging.md) | Debug execution issues | Fixing errors, unexpected behavior |
| [optimization.md](optimization.md) | Optimize for cost/latency/quality | Improving performance |
| [migration.md](migration.md) | Migrate/refactor projects | Upgrading, restructuring |

## Quick Reference

### Creating a New Crew

1. Define goal and success criteria
2. Identify required agents
3. Design tasks with dependencies
4. Choose process type
5. Create project structure
6. Configure YAML files
7. Implement crew class
8. Test and iterate

### Debugging Issues

1. Enable verbose mode
2. Gather error information
3. Reproduce the issue
4. Analyze traces
5. Identify root cause
6. Apply fix
7. Verify resolution

### Optimizing Performance

1. Collect baseline metrics
2. Identify bottlenecks
3. Choose optimization target
4. Apply strategies
5. Measure improvement
6. Iterate

### Migrating Projects

1. Backup existing project
2. Create target structure
3. Move/update files
4. Update imports
5. Test functionality
6. Clean up

## Process Selection

| Situation | Process |
|-----------|---------|
| New project | crew-creation.md |
| Errors occurring | debugging.md |
| Too slow/expensive | optimization.md |
| Restructuring needed | migration.md |
| Upgrading CrewAI | migration.md |
