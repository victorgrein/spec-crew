# CrewAI Development Platform

A comprehensive development platform for CrewAI projects with specialized agents, commands, and workflows.

## Overview

This platform provides a complete suite of tools for building, debugging, optimizing, and maintaining CrewAI projects. It includes specialized subagents, contextual documentation, and command-line interfaces for all CrewAI operations.

## Setup

### Prerequisites

- Python 3.7+
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the installer:
```bash
python install_config.py /path/to/your/project
```

Or run interactively:
```bash
python install_config.py
```

The installer creates `.opencode/` in your project and copies all configuration files with a summary of what was installed.

## Repository Structure

```
crewai-platform/
├── opencode/                   # Content to be installed as .opencode/
│   │   ├── agent/
│   │   ├── crewai-orchestrator.md    # Primary orchestrator agent (moved to root)
│   │   └── subagents/              # General-purpose subagents
│   │       ├── crewai/                # CrewAI specialized subagents
│   │       │   ├── agent-designer.md        # Create/configure agents
│   │       │   ├── crew-architect.md       # Design crew architectures
│   │       │   ├── crewai-documenter.md    # Generate documentation
│   │       │   ├── debugger.md             # Debug execution issues
│   │       │   ├── flow-engineer.md        # Create flows and state management
│   │       │   ├── llm-optimizer.md       # Optimize LLM configurations
│   │       │   ├── migration-specialist.md # Migrate/refactor projects
│   │       │   ├── performance-analyst.md  # Analyze performance metrics
│   │       │   ├── task-designer.md       # Design/configure tasks
│   │       │   └── tool-specialist.md     # Create/integrate tools
│   │       ├── code/                   # Code execution subagents
│   │       │   ├── coder-agent.md       # Execute coding tasks
│   │       │   ├── reviewer.md          # Code review
│   │       │   ├── tester.md           # Test authoring
│   │       │   └── build-agent.md      # Build validation
│   │       └── core/                  # Core utilities
│   │           └── contextscout.md     # Context discovery
```

## Quick Start

### Create a New Crew

```bash
/crew create "A research crew that analyzes AI trends and writes reports"
```

The orchestrator will:
1. Analyze your specification
2. Design crew architecture
3. Generate YAML configurations
4. Create Python code
5. Ask for LLM preferences
6. Request permission before creating files

### Available Commands

| Command | Description |
|---------|-------------|
| `/crew create` | Create new crew from specification |
| `/crew analyze` | Analyze crew architecture |
| `/crew debug` | Debug crew execution issues |
| `/crew diagram` | Generate architecture diagrams |
| `/crew docs` | Generate documentation |
| `/crew migrate` | Migrate/refactor projects |
| `/crew optimize` | Optimize crew performance |
| `/crew review` | Review crew architecture |

## Core Components

### CrewAI Orchestrator

The primary agent that coordinates all CrewAI operations:
- **Routes requests** to appropriate specialists
- **Loads context** from documentation
- **Delegates tasks** to specialized subagents
- **Validates outputs** against best practices
- **Synthesizes results** for presentation

### Specialized Subagents

#### Architecture & Design
- **@crew-architect** - Design crew architectures and review composition
- **@agent-designer** - Create and configure agents
- **@task-designer** - Design tasks with expected outputs
- **@tool-specialist** - Create and integrate tools

#### Implementation
- **@coder-agent** - Execute coding tasks
- **@reviewer** - Code review and quality assurance
- **@tester** - Test authoring and TDD
- **@build-agent** - Build validation

#### Operations
- **@flow-engineer** - Create flows and manage state
- **@debugger** - Analyze and fix execution issues
- **@performance-analyst** - Analyze performance metrics
- **@llm-optimizer** - Optimize LLM configurations
- **@migration-specialist** - Migrate and refactor projects

#### Documentation
- **@crewai-documenter** - Generate documentation and diagrams

#### Utilities
- **@contextscout** - Discover and retrieve context files

## Context System

The platform uses a comprehensive context system organized by domain:

### CrewAI Context
Complete documentation for CrewAI concepts, processes, and standards.

### Task Management Context
Guides and standards for task breakdown and tracking.

## Workflows

Predefined workflows for common operations:
- **Create Crew** - Complete crew creation pipeline
- **Create Flow** - Flow development workflow
- **Debug Crew** - Systematic debugging process
- **Migrate Project** - Project migration procedures
- **Optimize Crew** - Performance optimization workflow

## Task Management

The platform includes a task management system for breaking down features into atomic subtasks with:
- **Dependency tracking** - Map task dependencies
- **Status management** - Track progress
- **Parallel execution** - Identify parallelizable tasks
- **Validation** - Ensure task completeness

## Features

### Intelligent Agent Composition
- Automatic agent role and goal generation
- Tool assignment based on requirements
- LLM configuration recommendations
- Collaboration pattern suggestions

### Code Generation
- YAML configuration generation
- Python crew implementation
- Flow state management
- Tool integration templates

### Quality Assurance
- Architecture review checklist
- Code review standards
- Performance optimization
- Security best practices

### Documentation
- Automatic documentation generation
- Architecture diagrams
- API documentation
- Usage examples

## Development Workflow

1. **Specify** - Describe your crew/flow requirements
2. **Design** - Orchestrator analyzes and designs architecture
3. **Generate** - Subagents create configurations and code
4. **Review** - Reviewer validates quality
5. **Test** - Tester creates tests
6. **Deploy** - Ready-to-run project

## Best Practices

### Crew Design
- Use clear agent roles and goals
- Define appropriate tools for each agent
- Choose process type based on task dependencies
- Configure memory for complex workflows

### Code Quality
- Follow modular architecture
- Implement error handling
- Add comprehensive tests
- Document key decisions

### Performance
- Configure `max_rpm` to avoid rate limits
- Enable caching for expensive operations
- Use appropriate `max_iter` values
- Monitor token usage

## Requirements

- CrewAI framework
- Python 3.8+
- OpenAI or Anthropic API access (for LLMs)
- Bun (for package management)

## Contributing

This is a development platform for CrewAI projects. To contribute:

1. Add new subagents to appropriate directories
2. Update context documentation
3. Create or update workflows
4. Follow existing patterns and standards

## License

[Add your license here]

## Support

For issues or questions related to:
- **CrewAI Framework**: https://github.com/crewAIInc/crewAI
- **This Platform**: Check context/crewai/ for detailed documentation
