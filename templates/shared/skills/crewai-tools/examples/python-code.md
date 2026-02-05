# CrewAI Tools - Python Code Examples

Python examples and implementation snippets for `crewai-tools`.

## Extracted Python Snippets

### Python Example 1

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

### Python Example 2

```python
from crewai.tools import tool

@tool("calculate_metrics")
def calculate_metrics(data: str) -> str:
    """Calculate key metrics from the provided data.
    
    Use this when you need to compute statistics or metrics.
    
    Args:
        data: JSON string containing the data to analyze
    """
    try:
        import json
        parsed = json.loads(data)
        # Calculate metrics
        return f"Metrics calculated: {metrics}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### Python Example 3

```python
@tool("fetch_data_async")
async def fetch_data_async(query: str) -> str:
    """Asynchronously fetch data based on the query."""
    await asyncio.sleep(1)  # Simulate async operation
    return f"Data retrieved for {query}"
```

### Python Example 4

```python
class AsyncAPITool(BaseTool):
    name: str = "async_api_tool"
    description: str = "Fetches data from external API asynchronously"

    async def _run(self, endpoint: str) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                data = await response.json()
                return str(data)
```

### Python Example 5

```python
@tool
def expensive_operation(query: str) -> str:
    """Performs an expensive operation."""
    return result

def cache_func(args, result):
    # Only cache if result doesn't contain error
    return "error" not in result.lower()

expensive_operation.cache_function = cache_func
```

### Python Example 6

```python
from crewai import Agent
from crewai_tools import SerperDevTool, FileReadTool

search_tool = SerperDevTool()
file_tool = FileReadTool()

researcher = Agent(
    role="Research Analyst",
    goal="Find and analyze information",
    backstory="Expert researcher",
    tools=[search_tool, file_tool],
    verbose=True
)
```

### Python Example 7

```python
description = """
Use this tool to search the web for current information.
Best for: Finding recent news, articles, and data.
Input: A search query string.
Output: List of relevant search results with titles and snippets.
"""
```

### Python Example 8

```python
description = "Searches the web"  # Too vague
```

### Python Example 9

```python
from pydantic import BaseModel, Field
from typing import Type

class MyToolInput(BaseModel):
    """Input schema for MyTool."""
    query: str = Field(..., description="The search query")
    limit: int = Field(default=10, description="Max results to return")

class MyCustomTool(BaseTool):
    name: str = "my_custom_tool"
    description: str = "Searches for data"
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, query: str, limit: int = 10) -> str:
        try:
            results = self._perform_search(query)
            return f"Results: {results}"
        except Exception as e:
            return f"Error: {str(e)}"
```
