# CrewAI Processes - Basic Setup

Minimal setup path for `crewai-processes` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[research_task, write_task, edit_task],
    process=Process.sequential  # Default
)
```

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
