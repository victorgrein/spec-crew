# CrewAI Tasks - YAML Configuration Examples

YAML configuration patterns for `crewai-tasks`.

## Extracted YAML Snippets

### YAML Example 1

```yaml
# config/tasks.yaml
research_task:
  description: >
    Research the latest developments in {topic} from the past month.
    Focus on peer-reviewed sources and industry reports.
  expected_output: >
    A comprehensive report of 500-800 words covering:
    1) Key findings
    2) Market implications
    3) Recommended actions
    Use markdown formatting.
  agent: researcher

analysis_task:
  description: >
    Analyze the research findings and identify key patterns.
  expected_output: >
    An analysis report with insights and recommendations.
  agent: analyst
  context:
    - research_task
```

### YAML Example 2

```yaml
task_name:
  description: >
    {Clear, detailed description of what needs to be done}
  expected_output: >
    {Specific description of the deliverable}
  agent: {agent_name}
```

### YAML Example 3

```yaml
task_name:
  description: >
    {Description}
  expected_output: >
    {Expected output}
  agent: {agent_name}
  context:
    - {previous_task_1}
    - {previous_task_2}
```

### YAML Example 4

```yaml
task_name:
  description: >
    {Description}
  expected_output: >
    {Expected output}
  agent: {agent_name}
  output_file: output/{filename}.md
```

### YAML Example 5

```yaml
research_task:
  description: >
    Research {topic} thoroughly using web searches and
    authoritative sources. Focus on:
    1. Recent developments (last 6 months)
    2. Key players and their contributions
    3. Market trends and predictions
    4. Expert opinions and analysis
    Include citations for all major claims.
  expected_output: >
    A comprehensive research report (800-1200 words) containing:
    - Executive summary (100 words)
    - Key findings (5+ bullet points)
    - Detailed analysis (500-800 words)
    - Sources cited (minimum 3 authoritative sources)
    Format: Markdown with clear headers
  agent: researcher
```

### YAML Example 6

```yaml
analysis_task:
  description: >
    Analyze the research findings and identify:
    1. Key patterns and trends
    2. Opportunities and risks
    3. Actionable recommendations
    Base your analysis on the research provided.
  expected_output: >
    An analysis report containing:
    - Key insights (3-5 major findings)
    - Supporting evidence for each insight
    - Risk assessment
    - Actionable recommendations (3-5 items)
    Format: Structured markdown with sections
  agent: analyst
  context:
    - research_task
```

### YAML Example 7

```yaml
writing_task:
  description: >
    Write an engaging article about {topic} based on the
    research and analysis provided. The article should:
    1. Be accessible to a general audience
    2. Include concrete examples
    3. Have a clear narrative flow
    4. End with actionable takeaways
  expected_output: >
    A well-structured article (1000-1500 words) containing:
    - Compelling introduction
    - 3-4 main sections with headers
    - Concrete examples and data points
    - Strong conclusion with takeaways
    Format: Markdown, ready for publication
  agent: writer
  context:
    - research_task
    - analysis_task
  output_file: output/article.md
```

### YAML Example 8

```yaml
review_task:
  description: >
    Review the content for:
    1. Accuracy of information
    2. Clarity of writing
    3. Logical flow and structure
    4. Grammar and style
    Provide specific, actionable feedback.
  expected_output: >
    A review report containing:
    - Overall quality score (1-10)
    - Strengths (3+ points)
    - Areas for improvement (specific issues)
    - Suggested revisions (with examples)
    Format: Structured feedback document
  agent: reviewer
  context:
    - writing_task
```

### YAML Example 9

```yaml
extraction_task:
  description: >
    Extract structured data from the provided content.
    Identify and extract:
    1. Key entities (people, organizations, products)
    2. Important dates and numbers
    3. Relationships between entities
    4. Key metrics and statistics
  expected_output: >
    Structured data in JSON format containing:
    - entities: list of identified entities
    - metrics: key numbers and statistics
    - relationships: connections between entities
    - timeline: important dates and events
  agent: analyst
  context:
    - research_task
```

### YAML Example 10

```yaml
summary_task:
  description: >
    Create a concise summary of the main findings.
    The summary should:
    1. Capture the most important points
    2. Be understandable without reading the full report
    3. Include key data points
    4. Highlight actionable items
  expected_output: >
    An executive summary (200-300 words) containing:
    - Main findings (3-5 bullet points)
    - Key data points
    - Primary recommendation
    Format: Concise, scannable text
  agent: writer
  context:
    - research_task
    - analysis_task
```

### YAML Example 11

```yaml
research_task:
  description: >
    Research {topic} for the {audience} audience.
    Focus on {focus_area}.
  expected_output: >
    Report on {topic} tailored for {audience}.
  agent: researcher
```
