# CrewAI Tools

> Source: Official CrewAI Documentation

## Overview

CrewAI tools empower agents with capabilities ranging from web searching and data analysis to collaboration and delegating tasks among coworkers.

## Key Characteristics

- **Utility**: Tasks like web searching, data analysis, content generation
- **Integration**: Seamlessly integrate into agent workflows
- **Customizability**: Create custom tools or use existing ones
- **Error Handling**: Robust error handling mechanisms
- **Caching**: Intelligent caching to optimize performance
- **Async Support**: Both synchronous and asynchronous tools

## Installation

```bash
pip install 'crewai[tools]'
```

## Built-in Tools

### Search & Research

| Tool | Description |
|------|-------------|
| `SerperDevTool` | Web search via Serper API |
| `WebsiteSearchTool` | RAG-based website search |
| `GithubSearchTool` | Search GitHub repositories |
| `WikipediaTools` | Wikipedia search |
| `YoutubeChannelSearchTool` | YouTube channel search |
| `YoutubeVideoSearchTool` | YouTube video search |
| `EXASearchTool` | Exhaustive data source search |

### File & Document

| Tool | Description |
|------|-------------|
| `FileReadTool` | Read file contents |
| `FileWriteTool` | Write to files |
| `DirectoryReadTool` | Read directory contents |
| `DirectorySearchTool` | Search within directories |
| `PDFSearchTool` | Search PDF documents |
| `CSVSearchTool` | Search CSV files |
| `JSONSearchTool` | Search JSON files |
| `DOCXSearchTool` | Search Word documents |
| `TXTSearchTool` | Search text files |
| `MDXSearchTool` | Search Markdown files |
| `XMLSearchTool` | Search XML files |

### Database

| Tool | Description |
|------|-------------|
| `PGSearchTool` | PostgreSQL search |
| `MySQLTool` | MySQL operations |
| `NL2SQLTool` | Natural language to SQL |

### Web Scraping

| Tool | Description |
|------|-------------|
| `ScrapeWebsiteTool` | Scrape entire websites |
| `ScrapeElementFromWebsiteTool` | Scrape specific elements |
| `SeleniumScrapingTool` | Browser-based scraping |
| `FirecrawlScrapeWebsiteTool` | Firecrawl scraping |
| `FirecrawlCrawlWebsiteTool` | Firecrawl crawling |

### AI & Code

| Tool | Description |
|------|-------------|
| `CodeInterpreterTool` | Execute Python code |
| `RagTool` | General RAG operations |
| `VisionTool` | Image analysis |
| `DALL-E Tool` | Image generation |
| `LlamaIndexTool` | LlamaIndex integration |

## Creating Custom Tools

### Using BaseTool Subclass

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

### Using @tool Decorator

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

## Async Tools

### Async with Decorator

```python
@tool("fetch_data_async")
async def fetch_data_async(query: str) -> str:
    """Asynchronously fetch data based on the query."""
    await asyncio.sleep(1)  # Simulate async operation
    return f"Data retrieved for {query}"
```

### Async with BaseTool

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

## Custom Caching

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

## Using Tools with Agents

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

## Best Practices

1. **Clear Descriptions**: Agents use descriptions to decide which tool to use
2. **Error Handling**: Always wrap operations in try/except, return error strings
3. **Input Validation**: Use Pydantic models with Field descriptions
4. **Caching**: Enable for expensive operations
5. **Async**: Use for I/O-bound operations
6. **Rate Limiting**: Consider API limits in tool implementation

## Tool Description Guidelines

Good description:
```python
description = """
Use this tool to search the web for current information.
Best for: Finding recent news, articles, and data.
Input: A search query string.
Output: List of relevant search results with titles and snippets.
"""
```

Bad description:
```python
description = "Searches the web"  # Too vague
```
