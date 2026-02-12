#!/usr/bin/env python3
"""Generate agent or task configuration interactively."""

import yaml
from pathlib import Path
from typing import Dict, Any, List


def get_input(prompt: str, required: bool = True, default: str = None) -> str:
    """Get input from user with optional default."""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "

    value = input(full_prompt).strip()

    if not value and default:
        return default

    if required and not value:
        print("This field is required.")
        return get_input(prompt, required, default)

    return value


def get_multiline_input(prompt: str) -> str:
    """Get multiline input from user."""
    print(f"{prompt} (Enter blank line to finish):")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines)


def get_list_input(prompt: str) -> List[str]:
    """Get a list of items from user."""
    items = []
    print(f"{prompt} (Enter blank line to finish):")
    while True:
        item = input("  > ").strip()
        if not item:
            break
        items.append(item)
    return items


def get_boolean_input(prompt: str, default: bool = False) -> bool:
    """Get boolean input from user."""
    default_str = "Y/n" if default else "y/N"
    value = input(f"{prompt} [{default_str}]: ").strip().lower()

    if not value:
        return default

    return value in ["y", "yes", "true", "1"]


def generate_agent() -> Dict[str, Any]:
    """Interactive agent configuration generator."""
    print("\n" + "=" * 50)
    print("AGENT CONFIGURATION GENERATOR")
    print("=" * 50 + "\n")

    agent_name = get_input("Agent name (e.g., 'researcher')")

    print("\n--- Core Attributes (Required) ---")
    role = get_input("Role/title", default="Specialist")
    goal = get_input("Goal/objective")
    backstory = get_multiline_input("Backstory/personality")

    agent_config = {"role": role, "goal": goal, "backstory": backstory}

    print("\n--- Optional Configuration ---")

    # LLM
    if get_boolean_input("Configure LLM?", default=False):
        llm = get_input("LLM model", default="gpt-4")
        agent_config["llm"] = llm

    # Verbose
    verbose = get_boolean_input("Enable verbose logging?", default=True)
    if verbose:
        agent_config["verbose"] = True

    # Tools
    if get_boolean_input("Add tools?", default=False):
        tools = get_list_input("Enter tool names")
        if tools:
            agent_config["tools"] = tools

    # Allow delegation
    allow_delegation = get_boolean_input(
        "Allow delegation to other agents?", default=True
    )
    if not allow_delegation:
        agent_config["allow_delegation"] = False

    # Memory
    memory = get_boolean_input("Enable memory?", default=True)
    if not memory:
        agent_config["memory"] = False

    # Max iterations
    max_iter = get_input("Max iterations (default: 25)", required=False, default="25")
    if max_iter != "25":
        agent_config["max_iterations"] = int(max_iter)

    # Max retries
    max_retries = get_input("Max retries (default: 2)", required=False, default="2")
    if max_retries != "2":
        agent_config["max_retry_limit"] = int(max_retries)

    return {agent_name: agent_config}


def generate_task() -> Dict[str, Any]:
    """Interactive task configuration generator."""
    print("\n" + "=" * 50)
    print("TASK CONFIGURATION GENERATOR")
    print("=" * 50 + "\n")

    task_name = get_input("Task name (e.g., 'research_task')")

    print("\n--- Core Attributes (Required) ---")
    description = get_multiline_input("Task description")
    expected_output = get_multiline_input("Expected output")
    agent = get_input("Assigned agent name")

    task_config = {
        "description": description,
        "expected_output": expected_output,
        "agent": agent,
    }

    print("\n--- Optional Configuration ---")

    # Context dependencies
    if get_boolean_input("Add context dependencies?", default=False):
        context = get_list_input("Enter task names this depends on")
        if context:
            task_config["context"] = context

    # Output file
    if get_boolean_input("Save output to file?", default=False):
        output_file = get_input("Output file path", default="output/result.md")
        task_config["output_file"] = output_file

    # Markdown
    markdown = get_boolean_input("Format as markdown?", default=True)
    if markdown:
        task_config["markdown"] = True

    # Async mode
    if get_boolean_input("Run asynchronously?", default=False):
        task_config["async_mode"] = True
        workers = get_input("Max workers (default: 4)", required=False, default="4")
        if workers != "4":
            task_config["max_workers"] = int(workers)

    # Timeout
    if get_boolean_input("Set timeout?", default=False):
        timeout = get_input("Timeout in seconds", default="600")
        task_config["timeout"] = int(timeout)

    # Guardrails
    if get_boolean_input("Add guardrails?", default=False):
        guardrails = get_list_input("Enter guardrail rules")
        if guardrails:
            task_config["guardrails"] = guardrails

    return {task_name: task_config}


def main():
    """Main CLI interface."""
    import sys

    print("\n" + "=" * 50)
    print("CREWAI CONFIGURATION GENERATOR")
    print("=" * 50)

    print("\nWhat would you like to generate?")
    print("  1. Agent configuration")
    print("  2. Task configuration")
    print("  3. Both (full crew setup)")

    choice = input("\nEnter choice (1/2/3): ").strip()

    all_configs = {}

    if choice == "1":
        agent_config = generate_agent()
        all_configs.update(agent_config)
        output_file = "agents.yaml"

    elif choice == "2":
        task_config = generate_task()
        all_configs.update(task_config)
        output_file = "tasks.yaml"

    elif choice == "3":
        print("\n--- Agents ---")
        num_agents = int(get_input("How many agents?", default="2"))
        for i in range(num_agents):
            print(f"\nAgent {i + 1}/{num_agents}")
            agent_config = generate_agent()
            all_configs.update(agent_config)

        print("\n--- Tasks ---")
        num_tasks = int(get_input("How many tasks?", default="2"))
        for i in range(num_tasks):
            print(f"\nTask {i + 1}/{num_tasks}")
            task_config = generate_task()
            all_configs.update(task_config)

        output_file = "crew_config.yaml"

    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

    # Generate YAML
    yaml_content = yaml.dump(all_configs, default_flow_style=False, sort_keys=False)

    print("\n" + "=" * 50)
    print("GENERATED CONFIGURATION")
    print("=" * 50)
    print(yaml_content)

    # Save to file
    save = get_boolean_input(f"\nSave to {output_file}?", default=True)
    if save:
        output_path = Path(output_file)

        # Check if file exists
        if output_path.exists():
            overwrite = get_boolean_input(
                f"{output_file} exists. Overwrite?", default=False
            )
            if not overwrite:
                output_file = get_input("New filename", default=f"new_{output_file}")
                output_path = Path(output_file)

        output_path.write_text(yaml_content)
        print(f"✅ Configuration saved to: {output_path.absolute()}")
    else:
        print("Configuration not saved.")


if __name__ == "__main__":
    main()
