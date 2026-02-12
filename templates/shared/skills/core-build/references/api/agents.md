# Agent Attributes Reference

Complete reference of all Agent configuration attributes in CrewAI.

## Required Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `role` | str | - | The agent's job title or function. Defines what the agent does. |
| `goal` | str | - | The agent's primary objective. What they aim to achieve. |
| `backstory` | str | - | Context and personality for the agent. Influences behavior and style. |

## Optional Attributes

### LLM Configuration

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `llm` | str/LLM | gpt-4 | Language model to use. Can be provider/model format. |
| `function_calling_llm` | str/LLM | None | Separate LLM for tool/function calling |
| `system_template` | str | None | Custom system prompt template |
| `prompt_template` | str | None | Custom user prompt template |

### Execution Control

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `verbose` | bool | False | Enable detailed logging of agent actions |
| `max_iterations` | int | 25 | Maximum iterations before giving up |
| `max_retry_limit` | int | 2 | Maximum retries on failure |
| `allow_delegation` | bool | True | Allow agent to delegate to other agents |
| `cache` | bool | True | Enable response caching |
| `step_callback` | Callable | None | Function called after each step |

### Tool Configuration

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `tools` | List[Tool] | [] | List of tools available to the agent |
| `tools_handler` | Callable | None | Custom tool execution handler |

### Memory and Context

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `memory` | bool | True | Enable long-term memory |
| `max_rpm` | int | None | Rate limit in requests per minute |

## Attribute Details

### Role

The role defines the agent's identity and capabilities. Best practices:
- Be specific about expertise level (e.g., "Senior" vs "Junior")
- Include domain specialization
- Mention unique skills or perspectives

Example:
```yaml
role: >
  Senior Software Architect specializing in 
  distributed systems and microservices
```

### Goal

The goal should be:
- Specific and measurable
- Achievable within agent capabilities
- Clear about expected outcomes

Example:
```yaml
goal: >
  Design a scalable microservices architecture
  that can handle 10,000 concurrent users
  with < 100ms response time
```

### Backstory

The backstory provides context and personality:
- Professional background
- Notable achievements
- Working style and preferences
- Communication style

Example:
```yaml
backstory: >
  You are a seasoned architect with 15 years
  of experience building systems at scale.
  You worked at Google and AWS, and you've
  led teams through multiple successful launches.
  You communicate clearly and prefer simple
  solutions over complex ones.
```

## LLM Providers

Supported LLM provider formats:

| Provider | Format Example |
|----------|---------------|
| OpenAI | `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo` |
| Anthropic | `anthropic/claude-3-opus`, `anthropic/claude-3-sonnet` |
| Azure | `azure/gpt-4` |
| Google | `google/gemini-pro` |
| Ollama | `ollama/llama2`, `ollama/mistral` |
| Local | `local/model-name` |

## Usage Examples

### Basic Agent
```yaml
researcher:
  role: Research Specialist
  goal: Find accurate information
  backstory: Expert researcher
```

### Advanced Agent
```yaml
senior_analyst:
  role: Senior Financial Analyst
  goal: Analyze market trends
  backstory: 10 years experience
  llm: gpt-4
  verbose: true
  tools:
    - web_search
    - calculator
  allow_delegation: false
  max_iterations: 30
```
