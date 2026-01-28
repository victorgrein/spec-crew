# CrewAI Standards Navigation

## Overview

Quality standards and best practices for CrewAI development.

## Available Standards

| File | Description | When to Use |
|------|-------------|-------------|
| [code-quality.md](code-quality.md) | Code quality standards | Writing/reviewing code |
| [project-structure.md](project-structure.md) | Project structure standards | Setting up projects |

## Quick Reference

### Code Quality Checklist

- [ ] Project follows standard structure
- [ ] Naming conventions followed
- [ ] Agents have detailed roles, goals, backstories
- [ ] Tasks have clear descriptions and expected outputs
- [ ] Tools have proper error handling
- [ ] Environment variables documented
- [ ] README.md complete
- [ ] Tests included

### Project Structure Checklist

- [ ] Standard directory structure
- [ ] YAML configs for agents/tasks
- [ ] Custom tools in tools/ directory
- [ ] Tests in tests/ directory
- [ ] pyproject.toml configured
- [ ] .env for environment variables
- [ ] .gitignore configured

## Standards Summary

### Naming Conventions

| Component | Convention | Example |
|-----------|------------|---------|
| Project | snake_case | `my_crew_project` |
| Crew class | PascalCase | `ResearchCrew` |
| Agent methods | snake_case | `research_analyst` |
| Task methods | snake_case | `research_task` |
| Tool classes | PascalCase | `CustomSearchTool` |

### Required Files

**Crew Project:**
- main.py
- crew.py
- config/agents.yaml
- config/tasks.yaml
- pyproject.toml
- README.md

**Flow Project:**
- main.py
- crews/{crew_name}/{crew_name}.py
- crews/{crew_name}/config/agents.yaml
- crews/{crew_name}/config/tasks.yaml
- pyproject.toml
- README.md
