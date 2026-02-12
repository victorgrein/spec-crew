#!/usr/bin/env python3
"""Enhanced validation for CrewAI crew configuration files."""

import yaml
import sys
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional


class ValidationError:
    """Represents a validation error with location information."""
    
    def __init__(self, file: str, line: int, message: str, suggestion: str = ""):
        self.file = file
        self.line = line
        self.message = message
        self.suggestion = suggestion
    
    def __str__(self):
        location = f"{self.file}:{self.line}" if self.line > 0 else self.file
        msg = f"  ❌ {location} - {self.message}"
        if self.suggestion:
            msg += f"\n     💡 {self.suggestion}"
        return msg


def find_line_number(content: str, key: str, parent_key: str = "") -> int:
    """Find the line number of a key in YAML content."""
    lines = content.split('\n')
    
    if parent_key:
        # Find parent first, then key within it
        in_parent = False
        parent_indent = -1
        
        for i, line in enumerate(lines, 1):
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            
            if stripped.startswith(f"{parent_key}:"):
                in_parent = True
                parent_indent = indent
                continue
            
            if in_parent:
                if stripped.startswith(f"{key}:"):
                    return i
                # Check if we've exited the parent block
                if stripped and not stripped.startswith('#') and parent_indent >= 0 and indent <= parent_indent:
                    in_parent = False
    else:
        # Direct key search
        for i, line in enumerate(lines, 1):
            if line.lstrip().startswith(f"{key}:"):
                return i
    
    return 0


def validate_yaml_syntax(file_path: Path) -> Tuple[bool, List[ValidationError], str]:
    """Validate YAML syntax and return content if valid."""
    errors = []
    content = ""
    
    try:
        content = file_path.read_text()
        yaml.safe_load(content)
        return True, errors, content
    except yaml.YAMLError as e:
        error_msg = str(e)
        
        # Extract line number from YAML error
        line_match = re.search(r'line (\d+)', error_msg)
        line_num = int(line_match.group(1)) if line_match else 0
        
        suggestion = "Check for missing colons, incorrect indentation, or unmatched quotes"
        errors.append(ValidationError(
            file_path.name,
            line_num,
            f"YAML syntax error: {error_msg}",
            suggestion
        ))
        return False, errors, content
    except Exception as e:
        errors.append(ValidationError(
            file_path.name,
            0,
            f"Failed to read file: {e}"
        ))
        return False, errors, content


def validate_agents_yaml(file_path: Path) -> List[ValidationError]:
    """Validate agents.yaml structure with detailed error reporting."""
    errors = []
    
    # First validate YAML syntax
    is_valid, syntax_errors, content = validate_yaml_syntax(file_path)
    if not is_valid:
        return syntax_errors
    
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError:
        return errors  # Already caught above
    
    if not data:
        errors.append(ValidationError(
            file_path.name,
            0,
            "File is empty",
            "Add at least one agent definition"
        ))
        return errors
    
    if not isinstance(data, dict):
        errors.append(ValidationError(
            file_path.name,
            1,
            "Root must be a dictionary (agent names as keys)",
            "Format: agent_name:\n  role: ...\n  goal: ..."
        ))
        return errors
    
    required_agent_fields = ["role", "goal", "backstory"]
    optional_agent_fields = [
        "llm", "verbose", "tools", "memory", "allow_delegation",
        "max_iterations", "max_retry_limit", "cache", "max_rpm",
        "system_template", "prompt_template", "function_calling_llm"
    ]
    
    for agent_name, config in data.items():
        line_num = find_line_number(content, agent_name)
        
        if not isinstance(config, dict):
            errors.append(ValidationError(
                file_path.name,
                line_num,
                f"Agent '{agent_name}' must be a dictionary",
                f"Check indentation for '{agent_name}'"
            ))
            continue
        
        # Check required fields
        for field in required_agent_fields:
            if field not in config:
                field_line = find_line_number(content, field, agent_name)
                errors.append(ValidationError(
                    file_path.name,
                    field_line or line_num,
                    f"Agent '{agent_name}' missing required field '{field}'",
                    f"Add '{field}:>\n  Your {field} here'"
                ))
        
        # Check for unknown fields (potential typos)
        for field in config.keys():
            if field not in required_agent_fields and field not in optional_agent_fields:
                field_line = find_line_number(content, field, agent_name)
                suggestion = f"Did you mean one of: {', '.join(optional_agent_fields[:5])}...?"
                errors.append(ValidationError(
                    file_path.name,
                    field_line or line_num,
                    f"Agent '{agent_name}' has unknown field '{field}'",
                    suggestion
                ))
        
        # Validate field types
        if "verbose" in config and not isinstance(config["verbose"], bool):
            errors.append(ValidationError(
                file_path.name,
                find_line_number(content, "verbose", agent_name),
                f"Agent '{agent_name}': 'verbose' must be true or false"
            ))
        
        if "tools" in config and not isinstance(config["tools"], list):
            errors.append(ValidationError(
                file_path.name,
                find_line_number(content, "tools", agent_name),
                f"Agent '{agent_name}': 'tools' must be a list",
                "Format: tools:\n  - tool_name_1\n  - tool_name_2"
            ))
        
        if "max_iterations" in config:
            if not isinstance(config["max_iterations"], int) or config["max_iterations"] < 1:
                errors.append(ValidationError(
                    file_path.name,
                    find_line_number(content, "max_iterations", agent_name),
                    f"Agent '{agent_name}': 'max_iterations' must be a positive integer"
                ))
    
    return errors


def validate_tasks_yaml(file_path: Path, available_agents: List[str]) -> List[ValidationError]:
    """Validate tasks.yaml structure with detailed error reporting."""
    errors = []
    
    # First validate YAML syntax
    is_valid, syntax_errors, content = validate_yaml_syntax(file_path)
    if not is_valid:
        return syntax_errors
    
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError:
        return errors  # Already caught above
    
    if not data:
        errors.append(ValidationError(
            file_path.name,
            0,
            "File is empty",
            "Add at least one task definition"
        ))
        return errors
    
    if not isinstance(data, dict):
        errors.append(ValidationError(
            file_path.name,
            1,
            "Root must be a dictionary (task names as keys)",
            "Format: task_name:\n  description: ...\n  expected_output: ..."
        ))
        return errors
    
    required_task_fields = ["description", "expected_output", "agent"]
    optional_task_fields = [
        "context", "output_file", "output_json", "output_pydantic",
        "markdown", "async_mode", "timeout", "max_retries", "guardrails",
        "quality_check", "human_input", "callback", "parallel", "max_workers"
    ]
    
    available_tasks = list(data.keys())
    
    for task_name, config in data.items():
        line_num = find_line_number(content, task_name)
        
        if not isinstance(config, dict):
            errors.append(ValidationError(
                file_path.name,
                line_num,
                f"Task '{task_name}' must be a dictionary",
                f"Check indentation for '{task_name}'"
            ))
            continue
        
        # Check required fields
        for field in required_task_fields:
            if field not in config:
                field_line = find_line_number(content, field, task_name)
                errors.append(ValidationError(
                    file_path.name,
                    field_line or line_num,
                    f"Task '{task_name}' missing required field '{field}'",
                    f"Add '{field}:>\n  Your {field} here'"
                ))
        
        # Validate agent reference
        if "agent" in config:
            agent_ref = config["agent"]
            if available_agents and agent_ref not in available_agents:
                errors.append(ValidationError(
                    file_path.name,
                    find_line_number(content, "agent", task_name),
                    f"Task '{task_name}' references unknown agent '{agent_ref}'",
                    f"Available agents: {', '.join(available_agents)}"
                ))
        
        # Check for unknown fields
        for field in config.keys():
            if field not in required_task_fields and field not in optional_task_fields:
                field_line = find_line_number(content, field, task_name)
                suggestion = f"Did you mean one of: {', '.join(optional_task_fields[:5])}...?"
                errors.append(ValidationError(
                    file_path.name,
                    field_line or line_num,
                    f"Task '{task_name}' has unknown field '{field}'",
                    suggestion
                ))
        
        # Validate context dependencies
        if "context" in config:
            context = config["context"]
            if not isinstance(context, list):
                errors.append(ValidationError(
                    file_path.name,
                    find_line_number(content, "context", task_name),
                    f"Task '{task_name}': 'context' must be a list",
                    "Format: context:\n  - task_name_1\n  - task_name_2"
                ))
            else:
                for dep_task in context:
                    if dep_task not in available_tasks:
                        errors.append(ValidationError(
                            file_path.name,
                            find_line_number(content, "context", task_name),
                            f"Task '{task_name}' depends on unknown task '{dep_task}'",
                            f"Available tasks: {', '.join(available_tasks)}"
                        ))
        
        # Check for circular dependencies
        if "context" in config:
            visited = set()
            stack = [task_name]
            
            def check_circular(task: str, data: dict) -> Optional[str]:
                if task not in data:
                    return None
                task_config = data[task]
                if "context" not in task_config:
                    return None
                
                for dep in task_config["context"]:
                    if dep == task_name:
                        return dep
                    if dep in stack:
                        return dep
                    stack.append(dep)
                    result = check_circular(dep, data)
                    stack.pop()
                    if result:
                        return result
                return None
            
            circular = check_circular(task_name, data)
            if circular:
                errors.append(ValidationError(
                    file_path.name,
                    line_num,
                    f"Circular dependency detected: '{task_name}' <-> '{circular}'",
                    "Remove the circular reference in context"
                ))
        
        # Validate output_pydantic reference
        if "output_pydantic" in config:
            pydantic_model = config["output_pydantic"]
            # Note: We can't actually validate Python class existence from YAML
            # but we can warn if it looks suspicious
            if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', str(pydantic_model)):
                errors.append(ValidationError(
                    file_path.name,
                    find_line_number(content, "output_pydantic", task_name),
                    f"Task '{task_name}': 'output_pydantic' should be a valid Python class name",
                    f"Ensure '{pydantic_model}' is defined and imported in crew.py"
                ))
        
        # Validate output_file path
        if "output_file" in config:
            output_path = config["output_file"]
            if ".." in str(output_path):
                errors.append(ValidationError(
                    file_path.name,
                    find_line_number(content, "output_file", task_name),
                    f"Task '{task_name}': 'output_file' contains '..' which may be unsafe",
                    "Use relative paths within the project directory"
                ))
        
        # Validate async_mode
        if "async_mode" in config and not isinstance(config["async_mode"], bool):
            errors.append(ValidationError(
                file_path.name,
                find_line_number(content, "async_mode", task_name),
                f"Task '{task_name}': 'async_mode' must be true or false"
            ))
    
    return errors


def validate_crew_structure(crew_dir: Path) -> Tuple[List[ValidationError], List[str], List[str]]:
    """Validate complete crew structure."""
    all_errors = []
    available_agents = []
    available_tasks = []
    
    # Check for required files
    agents_file = crew_dir / "agents.yaml"
    tasks_file = crew_dir / "tasks.yaml"
    
    # Also check common alternative locations
    alt_locations = [
        crew_dir / "config" / "agents.yaml",
        crew_dir / "config" / "tasks.yaml",
    ]
    
    # Try to find agents.yaml
    if not agents_file.exists():
        for alt in alt_locations:
            if "agents.yaml" in str(alt) and alt.exists():
                agents_file = alt
                break
    
    # Try to find tasks.yaml
    if not tasks_file.exists():
        for alt in alt_locations:
            if "tasks.yaml" in str(alt) and alt.exists():
                tasks_file = alt
                break
    
    if not agents_file.exists():
        all_errors.append(ValidationError(
            "agents.yaml",
            0,
            "agents.yaml not found in crew directory",
            f"Create {crew_dir / 'agents.yaml'} or {crew_dir / 'config' / 'agents.yaml'}"
        ))
    else:
        # Validate agents and collect agent names
        all_errors.extend(validate_agents_yaml(agents_file))
        try:
            with open(agents_file) as f:
                data = yaml.safe_load(f)
                if data and isinstance(data, dict):
                    available_agents = list(data.keys())
        except:
            pass
    
    if not tasks_file.exists():
        all_errors.append(ValidationError(
            "tasks.yaml",
            0,
            "tasks.yaml not found in crew directory",
            f"Create {crew_dir / 'tasks.yaml'} or {crew_dir / 'config' / 'tasks.yaml'}"
        ))
    else:
        # Validate tasks with knowledge of available agents
        all_errors.extend(validate_tasks_yaml(tasks_file, available_agents))
        try:
            with open(tasks_file) as f:
                data = yaml.safe_load(f)
                if data and isinstance(data, dict):
                    available_tasks = list(data.keys())
        except:
            pass
    
    return all_errors, available_agents, available_tasks


def print_validation_summary(errors: List[ValidationError], 
                            agents: List[str], 
                            tasks: List[str],
                            crew_dir: Path):
    """Print validation summary report."""
    print("\n" + "=" * 70)
    print(f"CREW VALIDATION REPORT: {crew_dir}")
    print("=" * 70)
    
    if agents:
        print(f"\n📋 Found {len(agents)} agent(s):")
        for agent in agents:
            print(f"   • {agent}")
    
    if tasks:
        print(f"\n📋 Found {len(tasks)} task(s):")
        for task in tasks:
            print(f"   • {task}")
    
    if errors:
        print(f"\n❌ Found {len(errors)} error(s):\n")
        for error in errors:
            print(error)
        print("\n" + "=" * 70)
        print("VALIDATION FAILED - Please fix the errors above")
        print("=" * 70)
        return False
    else:
        print("\n" + "=" * 70)
        print("✅ All validations passed!")
        print("=" * 70)
        
        # Print crew summary
        if agents and tasks:
            print(f"\n🚀 Crew ready to execute!")
            print(f"   Run: crew.kickoff(inputs={{...}})")
        
        return True


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Enhanced CrewAI Configuration Validator")
        print("=" * 70)
        print("\nUsage:")
        print("  validate_crew.py <path_to_crew_directory>")
        print("\nExamples:")
        print("  validate_crew.py ./my_crew")
        print("  validate_crew.py /home/user/projects/research_crew")
        print("\nFeatures:")
        print("  ✓ YAML syntax validation with line numbers")
        print("  ✓ Required field checking")
        print("  ✓ Agent reference validation")
        print("  ✓ Task context dependency validation")
        print("  ✓ Circular dependency detection")
        print("  ✓ Type checking for configuration values")
        print("  ✓ Detailed error messages with suggestions")
        sys.exit(1)
    
    crew_dir = Path(sys.argv[1])
    
    if not crew_dir.exists():
        print(f"Error: Directory not found: {crew_dir}")
        sys.exit(1)
    
    if not crew_dir.is_dir():
        print(f"Error: Not a directory: {crew_dir}")
        sys.exit(1)
    
    errors, agents, tasks = validate_crew_structure(crew_dir)
    success = print_validation_summary(errors, agents, tasks, crew_dir)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
