# Repository Notes (zread MCP)

## Repository Inspected

- `crewAIInc/crewAI-tools`
- Accessed via zread MCP (`zread_get_repo_structure`, `zread_read_file`, `zread_search_doc`)

## Critical Note

The repository README includes a deprecation warning and points to:

- `https://github.com/crewAIInc/crewAI/tree/main/lib/crewai-tools`

Use this monorepo location as the long-term canonical implementation reference.

## High-Value Files Reviewed

- `README.md`
- `BUILDING_TOOLS.md`
- `crewai_tools/tools/file_read_tool/file_read_tool.py`
- `crewai_tools/tools/file_writer_tool/file_writer_tool.py`
- `crewai_tools/tools/serper_dev_tool/serper_dev_tool.py`

## Observed Repository Structure

- Root contains `README.md`, `BUILDING_TOOLS.md`, `pyproject.toml`, `tool.specs.json`, and tests
- Tool implementations live under `crewai_tools/tools/*`
- Adapters live under `crewai_tools/adapters/*`
- Tests live under `tests/tools/*` and related subpackages

## Conventions Observed in Source

### 1) Schema-first inputs

- Tools use Pydantic models for `args_schema`
- Input fields include descriptions and validation metadata

### 2) Metadata on tool classes

- Clear `name` and `description`
- Optional `env_vars` declarations (`EnvVar` objects)
- Optional `package_dependencies` declarations

### 3) Deterministic execution methods

- `_run(...)` implemented for synchronous execution
- `_arun(...)` added or delegated when async is needed

### 4) Failure handling style

- Return actionable error strings
- Catch and classify provider/network failures
- Avoid uncontrolled exception leakage in normal flow

### 5) Discovery and naming

- Tool classes end with `Tool`
- Module layout enables spec-generation and discovery scripts

## BUILDING_TOOLS.md Guidance Highlights

- Create folder: `crewai_tools/tools/<tool_name>/`
- Include class ending in `Tool` extending `BaseTool` or `RagTool`
- Define explicit `args_schema`
- Add tests and tool README
- Validate optional dependencies and document install extras
- Keep outputs concise and transcript-ready

## Practical Use in This Skill

- Treat docs pages as product-level source of truth
- Use repository patterns to shape code quality and implementation style
- Reconfirm assumptions against maintained monorepo path before shipping production integrations
