# CrewAI Tools - Complete Reference

This document centralizes detailed reference material for `crewai-tools` and supports progressive disclosure during skill execution.

## Source Material

- Core skill file: `../SKILL.md`
- Legacy reference files:
  - `tools-reference.md`

## Section Index from SKILL.md

- What This Skill Does
- When to Use This Skill
- Quick Reference
-   Key Characteristics
-   Installation
- Built-in Tools
-   Search & Research
-   File & Document
-   Database
-   Web Scraping
-   AI & Code
- Creating Custom Tools
-   Using BaseTool Subclass
-   Using @tool Decorator
- Async Tools
-   Async with Decorator
-   Async with BaseTool
- Custom Caching
- Using Tools with Agents
- Tool Description Guidelines
- Best Practices
- Related Skills

## Essential Attributes

The following tables were extracted from `SKILL.md` and should be considered the canonical attribute and option index for this phase.

### Table 1

| Tool | Description |
|------|-------------|
| `SerperDevTool` | Web search via Serper API |
| `WebsiteSearchTool` | RAG-based website search |
| `GithubSearchTool` | Search GitHub repositories |
| `WikipediaTools` | Wikipedia search |
| `EXASearchTool` | Exhaustive data source search |

### Table 2

| Tool | Description |
|------|-------------|
| `FileReadTool` | Read file contents |
| `FileWriteTool` | Write to files |
| `DirectoryReadTool` | Read directory contents |
| `PDFSearchTool` | Search PDF documents |
| `CSVSearchTool` | Search CSV files |
| `JSONSearchTool` | Search JSON files |

### Table 3

| Tool | Description |
|------|-------------|
| `PGSearchTool` | PostgreSQL search |
| `MySQLTool` | MySQL operations |
| `NL2SQLTool` | Natural language to SQL |

### Table 4

| Tool | Description |
|------|-------------|
| `ScrapeWebsiteTool` | Scrape entire websites |
| `SeleniumScrapingTool` | Browser-based scraping |
| `FirecrawlScrapeWebsiteTool` | Firecrawl scraping |

### Table 5

| Tool | Description |
|------|-------------|
| `CodeInterpreterTool` | Execute Python code |
| `RagTool` | General RAG operations |
| `VisionTool` | Image analysis |

## Edge Cases and Limitations

- Validate configuration compatibility before execution.
- Keep prompts concise to avoid context-window pressure.
- Add retries and guardrails for external tool/API calls.

## Common Pitfalls

| Problem | Cause | Solution |
|---|---|---|
| Ambiguous outcomes | Expected outputs are underspecified | Define concrete acceptance criteria and output format. |
| Execution drift | Role/task boundaries are unclear | Tighten role, goal, and task contracts. |
| Rework loops | Validation occurs too late | Add checkpoints and early review tasks. |
| Tool instability | Missing error handling and retries | Implement timeouts, retries, and fallback behavior. |

## Additional Notes

- This file is generated for Phase 4 standardization and can be expanded with skill-specific deep dives in later iterations.
