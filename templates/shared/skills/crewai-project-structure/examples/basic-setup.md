# CrewAI Project Structure - Basic Setup

Minimal setup path for `crewai-project-structure` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

```python
#!/usr/bin/env python
from my_crew.crew import MyCrew

def kickoff():
    """Run the crew."""
    inputs = {
        'topic': 'AI trends'
    }
    MyCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    kickoff()
```

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
