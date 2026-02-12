#!/usr/bin/env python3
"""Scaffold a new CrewAI Flow project."""

import argparse
import os
import shutil
import sys
from pathlib import Path


def scaffold_flow(
    project_name: str, target_dir: str | None = None, with_crew: bool = False
) -> Path:
    """Create a new flow project from template.

    Args:
        project_name: Name for the flow project
        target_dir: Target directory (default: current directory)
        with_crew: Whether to include crew integration placeholder

    Returns:
        Path to created project directory
    """
    # Validate project name
    if not project_name.replace("_", "").replace("-", "").isalnum():
        print(
            f"Error: Project name '{project_name}' must be alphanumeric with underscores or hyphens only"
        )
        sys.exit(1)

    # Determine target directory
    if target_dir:
        target_path = Path(target_dir).resolve() / project_name
    else:
        target_path = Path.cwd() / project_name

    # Check if directory already exists
    if target_path.exists():
        print(f"Error: Directory '{target_path}' already exists")
        sys.exit(1)

    # Get template path (relative to this script)
    script_dir = Path(__file__).parent.resolve()
    template_dir = script_dir.parent / "assets" / "starter"

    if not template_dir.exists():
        print(f"Error: Template directory '{template_dir}' not found")
        sys.exit(1)

    # Create project directory
    target_path.mkdir(parents=True, exist_ok=False)
    print(f"✓ Created project directory: {target_path}")

    # Copy template files
    for template_file in template_dir.iterdir():
        if template_file.is_file():
            # Read and replace placeholders
            content = template_file.read_text()

            # Replace placeholders
            class_name = "".join(
                word.capitalize() for word in project_name.replace("-", "_").split("_")
            )
            content = content.replace("GuideCreator", class_name)
            content = content.replace(
                "guide_creator", project_name.lower().replace("-", "_")
            )
            content = content.replace(
                "Guide Creator",
                project_name.replace("-", " ").replace("_", " ").title(),
            )

            # Determine output filename
            if template_file.name == "main.py":
                output_name = f"{project_name.lower().replace('-', '_')}_flow.py"
            else:
                output_name = template_file.name

            # Write file
            output_path = target_path / output_name
            output_path.write_text(content)
            print(f"✓ Created {output_name}")

    # Create additional directories
    (target_path / "data").mkdir(exist_ok=True)
    (target_path / "output").mkdir(exist_ok=True)
    (target_path / "tests").mkdir(exist_ok=True)

    # Create __init__.py for the tests directory
    (target_path / "tests" / "__init__.py").touch()

    if with_crew:
        # Create crew integration placeholder
        crew_file = target_path / "crew_placeholder.py"
        crew_content = f'''#!/usr/bin/env python3
"""Crew integration placeholder for {project_name} flow."""

from crewai import Agent, Task, Crew


class {class_name}Crew:
    """Crew placeholder - configure your agents and tasks here."""
    
    def __init__(self):
        self.agent = Agent(
            role="Assistant",
            goal="Help with the flow execution",
            backstory="An AI assistant supporting the flow"
        )
        
    def run(self, inputs=None):
        """Execute crew tasks."""
        # TODO: Implement crew logic
        pass
'''
        crew_file.write_text(crew_content)
        print(f"✓ Created crew_placeholder.py")

    # Create requirements.txt
    requirements = target_path / "requirements.txt"
    requirements.write_text("crewai\ncrewai-tools\n")
    print(f"✓ Created requirements.txt")

    # Create .gitignore
    gitignore = target_path / ".gitignore"
    gitignore.write_text(
        "__pycache__/\n*.pyc\n.env\n.venv/\nvenv/\noutput/\ndata/\n.DS_Store\n*.log\n"
    )
    print(f"✓ Created .gitignore")

    print(f"\n🚀 Project '{project_name}' scaffolded successfully!")
    print(f"\nNext steps:")
    print(f"  1. cd {target_path.name}")
    print(f"  2. pip install -r requirements.txt")
    print(f"  3. Review {output_name} and customize the flow logic")
    print(f"  4. Run: python {output_name}")

    if with_crew:
        print(f"  5. Edit crew_placeholder.py to configure your agents and tasks")

    return target_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scaffold a new CrewAI Flow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  scaffold_flow.py my_flow
  scaffold_flow.py research_flow --path /projects
  scaffold_flow.py my_flow --with-crew
        """,
    )
    parser.add_argument(
        "name", help="Flow project name (alphanumeric with underscores/hyphens)"
    )
    parser.add_argument("--path", help="Target directory (default: current directory)")
    parser.add_argument(
        "--with-crew", action="store_true", help="Include crew integration placeholder"
    )

    args = parser.parse_args()

    try:
        scaffold_flow(args.name, args.path, args.with_crew)
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
