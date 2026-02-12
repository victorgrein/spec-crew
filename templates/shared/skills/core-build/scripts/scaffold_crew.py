#!/usr/bin/env python3
"""Scaffold a new CrewAI crew project from templates."""

import argparse
import os
import shutil
from pathlib import Path

# Template directory relative to this script
TEMPLATE_DIR = Path(__file__).parent.parent / "assets" / "starter"


def create_file_from_template(
    template_path: Path, target_path: Path, replacements: dict
):
    """Create a file from template with placeholder replacements."""
    content = template_path.read_text()
    for key, value in replacements.items():
        content = content.replace(f"{{{key}}}", value)
    target_path.write_text(content)
    print(f"  Created: {target_path}")


def scaffold_crew(project_name: str, target_dir: str = ""):
    """Create a new crew project from templates.

    Args:
        project_name: Name of the crew project (used for class names)
        target_dir: Target directory (default: current directory)
    """
    # Validate project name
    if not project_name.replace("_", "").isalnum():
        print(
            f"Error: Project name '{project_name}' must be alphanumeric with underscores only"
        )
        return False

    # Determine target directory
    target_path: Path
    if not target_dir:
        target_path = Path.cwd() / project_name
    else:
        target_path = Path(target_dir) / project_name

    # Check if directory exists
    if target_path.exists():
        print(f"Error: Directory {target_path} already exists")
        return False

    print(f"Creating new crew project: {project_name}")
    print(f"Location: {target_path}")
    print("=" * 50)

    # Create directory structure
    target_path.mkdir(parents=True)
    (target_path / "config").mkdir()
    (target_path / "output").mkdir()
    print(f"Created directory structure")

    # Prepare replacements
    replacements = {
        "CrewName": project_name.title().replace("_", ""),
        "crew_name": project_name.lower().replace("_", "_"),
        "purpose": f"{project_name.title().replace('_', ' ')} operations",
    }

    # Copy template files
    template_files = {
        "config/agents.yaml": target_path / "config" / "agents.yaml",
        "config/tasks.yaml": target_path / "config" / "tasks.yaml",
        "crew.py": target_path / "crew.py",
        "main.py": target_path / "main.py",
        ".env.example": target_path / ".env.example",
        "README.md": target_path / "README.md",
    }

    for template_file, dest_path in template_files.items():
        template_path = TEMPLATE_DIR / template_file
        if template_path.exists():
            create_file_from_template(template_path, dest_path, replacements)
        else:
            print(f"  Warning: Template not found: {template_file}")

    # Create __init__.py
    (target_path / "__init__.py").touch()
    print(f"  Created: {target_path / '__init__.py'}")

    # Make main.py executable
    os.chmod(target_path / "main.py", 0o755)

    print("\n" + "=" * 50)
    print(f"✅ Crew project '{project_name}' created successfully!")
    print(f"\nNext steps:")
    print(f"  1. cd {project_name}")
    print(f"  2. cp .env.example .env  # Add your API keys")
    print(f"  3. pip install crewai crewai-tools")
    print(f"  4. python main.py 'your topic here'")
    print(f"\nProject structure:")
    for path in sorted(target_path.rglob("*")):
        if path.is_file():
            rel_path = path.relative_to(target_path)
            print(f"  {rel_path}")

    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scaffold a new CrewAI crew project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scaffold_crew.py my_research_crew
  python scaffold_crew.py content_team --path ./crews
  python scaffold_crew.py data_pipeline --path /home/user/projects
        """,
    )
    parser.add_argument(
        "name", help="Crew project name (alphanumeric with underscores)"
    )
    parser.add_argument(
        "--path", help="Target directory (default: current directory)", default=None
    )

    args = parser.parse_args()

    success = scaffold_crew(args.name, args.path)
    exit(0 if success else 1)
