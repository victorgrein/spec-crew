# Guide Creator Flow

A production-ready CrewAI Flow demonstrating state management, decorators, and persistence.

## Overview

This is a **Flow-first** example that showcases:
- **Structured state** with Pydantic models
- **Event-driven control** with @start and @listen decorators
- **Persistence** with @persist decorator
- **Direct LLM calls** for structured outputs
- **Crew integration** (crews created separately using core-build patterns)

## Architecture

```
Flow Layer (this project)
├── State Management (Pydantic models)
├── Orchestration Logic (@start, @listen decorators)
├── Routing & Control
└── Persistence

Crew Layer (separate project)
├── Agent Definitions (agents.yaml)
├── Task Definitions (tasks.yaml)
└── Crew Implementation (CrewBase)
```

**Note**: This flow references crews that should be created using the **core-build** skill patterns.

## Prerequisites

1. Install dependencies:
```bash
pip install crewai pydantic
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. (Optional) Create a crew using core-build skill:
```bash
# Use core-build skill to scaffold a crew
# Then reference it in main.py
```

## Usage

Run the flow:
```bash
python main.py
```

Visualize the flow:
```bash
python main.py plot
```

## Key Concepts Demonstrated

### 1. State Management
- **Structured state** with Pydantic BaseModel
- Type-safe field access
- Automatic state ID generation
- State persistence across executions

### 2. Decorators
- `@start()` - Entry point for flow execution
- `@listen()` - Event-driven step chaining
- `@persist()` - Automatic state persistence

### 3. Flow Patterns
- Sequential processing with state accumulation
- Iterative processing (section loop)
- Conditional logic (completion checking)
- Direct LLM calls for structured outputs

### 4. Persistence
- Class-level persistence with `@persist()`
- Automatic checkpointing after each method
- Resume capability on restart

## Output

- `output/guide_outline.json` - Structured outline
- `output/complete_guide.md` - Final compiled guide

## Integration with Crews

To integrate a real crew:

1. Create a crew using core-build skill patterns
2. Import the crew in `main.py`:
```python
from crews.content_crew.content_crew import ContentCrew
```
3. Call the crew in the `process_section` method:
```python
result = ContentCrew().crew().kickoff(inputs={
    "section_title": section.title,
    "section_description": section.description,
    "audience_level": self.state.audience_level
})
```

## Customization

- Modify `GuideCreatorState` to add custom fields
- Add new flow methods with @listen decorators
- Implement custom routing with @router
- Add human feedback gates

## Learning Path

1. **Start here**: Understand flow structure and state management
2. **Next**: Study templates in `assets/templates/`
3. **Then**: Review guides in `references/guides/`
4. **Finally**: Create your own flow using `scripts/scaffold_flow.py`
