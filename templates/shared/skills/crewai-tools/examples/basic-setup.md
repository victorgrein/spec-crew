# CrewAI Tools - Basic Setup

Minimal setup path for `crewai-tools` with the smallest useful starting point.

## Quick Start

1. Define the objective and expected output.
2. Apply the minimal configuration shown below.
3. Execute once and validate output quality.
4. Expand with patterns from `../references/patterns-reference.md`.

## Minimal Example

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type

class MyToolInput(BaseModel):
    """Input schema for MyTool."""
    query: str = Field(..., description="The search query")
    limit: int = Field(default=10, description="Max results to return")

class MyCustomTool(BaseTool):
    name: str = "my_custom_tool"
    description: str = """
    Searches for data based on query.
    Use this when you need to find specific information.
    """
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, query: str, limit: int = 10) -> str:
        try:
            # Tool implementation
            results = self._search(query, limit)
            return f"Found {len(results)} results: {results}"
        except Exception as e:
            return f"Error: {str(e)}"
```

## Next

- Add production-ready variants in `python-code.md` and `yaml-config.md`.
