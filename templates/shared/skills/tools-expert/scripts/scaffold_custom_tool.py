#!/usr/bin/env python3
"""Scaffold CrewAI custom tool boilerplate."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from textwrap import dedent


def normalize_identifier(raw: str) -> str:
    value = raw.strip().lower().replace("-", "_").replace(" ", "_")
    value = re.sub(r"[^a-z0-9_]", "", value)
    value = re.sub(r"_+", "_", value).strip("_")
    if not value:
        raise ValueError("Tool name must include letters or numbers")
    return value


def snake_to_camel(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_"))


def camel_to_words(value: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", " ", value)


def ensure_suffix(value: str, suffix: str) -> str:
    if value.endswith(suffix):
        return value
    return value + suffix


def build_env_lines(env_vars: list[str]) -> list[str]:
    if not env_vars:
        return ["    env_vars: List[EnvVar] = []"]

    lines = ["    env_vars: List[EnvVar] = ["]
    for env_var in env_vars:
        lines.append(
            f'        EnvVar(name="{env_var}", description="TODO: describe {env_var}", required=True),'
        )
    lines.append("    ]")
    return lines


def build_dependency_line(dependencies: list[str]) -> str:
    if not dependencies:
        return "    package_dependencies: List[str] = []"
    values = ", ".join(f'"{item}"' for item in dependencies)
    return f"    package_dependencies: List[str] = [{values}]"


def build_async_lines(with_async: bool) -> list[str]:
    if not with_async:
        return []
    return [
        "",
        "    async def _arun(self, query: str) -> str:",
        "        return self._run(query=query)",
    ]


def render_basetool(
    class_name: str,
    schema_name: str,
    display_name: str,
    description: str,
    env_vars: list[str],
    dependencies: list[str],
    with_async: bool,
) -> str:
    lines = [
        "from typing import Any, List, Type",
        "import os",
        "",
        "from crewai.tools import BaseTool, EnvVar",
        "from pydantic import BaseModel, Field",
        "",
        "",
        f"class {schema_name}(BaseModel):",
        f'    """Input schema for {class_name}."""',
        "",
        f'    query: str = Field(..., description="Primary input for {class_name}.")',
        "",
        "",
        f"class {class_name}(BaseTool):",
        f'    name: str = "{display_name}"',
        f'    description: str = "{description}"',
        f"    args_schema: Type[BaseModel] = {schema_name}",
    ]

    lines.extend(build_env_lines(env_vars))
    lines.append(build_dependency_line(dependencies))

    lines.extend(
        [
            "",
            "    def __init__(self, **kwargs: Any) -> None:",
            "        super().__init__(**kwargs)",
            "        self._validate_env_vars()",
            "",
            "    def _validate_env_vars(self) -> None:",
            "        missing = [",
            "            item.name",
            "            for item in self.env_vars",
            "            if item.required and item.name not in os.environ",
            "        ]",
            "        if missing:",
            '            missing_text = ", ".join(missing)',
            "            raise ValueError(",
            '                "Missing required environment variables: " + missing_text',
            "            )",
            "",
            "    def _run(self, query: str) -> str:",
            '        """Run the tool synchronously."""',
            f'        return "TODO: implement {class_name} for query: " + query',
        ]
    )

    lines.extend(build_async_lines(with_async))
    return "\n".join(lines) + "\n"


def render_decorator(
    function_name: str,
    display_name: str,
    description: str,
    with_async: bool,
) -> str:
    if with_async:
        return dedent(
            f"""\
            from crewai.tools import tool


            @tool("{display_name}")
            async def {function_name}(query: str) -> str:
                \"\"\"{description}\"\"\"
                return "TODO: implement async {function_name} for query: " + query
            """
        )

    return dedent(
        f"""\
        from crewai.tools import tool


        @tool("{display_name}")
        def {function_name}(query: str) -> str:
            \"\"\"{description}\"\"\"
            return "TODO: implement {function_name} for query: " + query
        """
    )


def render_readme(
    class_or_function_name: str,
    style: str,
    env_vars: list[str],
    dependencies: list[str],
) -> str:
    env_section = "\n".join(f"- `{name}`" for name in env_vars) or "- None"
    dep_section = "\n".join(f"- `{name}`" for name in dependencies) or "- None"

    usage_line = f"from my_tool import {class_or_function_name}\n" + (
        f"tool = {class_or_function_name}()"
        if style == "basetool"
        else f"tool = {class_or_function_name}"
    )

    return dedent(
        f"""\
        # {class_or_function_name}

        ## Style

        - `{style}`

        ## Environment Variables

        {env_section}

        ## Dependencies

        {dep_section}

        ## Usage

        ```python
        {usage_line}
        ```

        ## Notes

        - Add deterministic error handling before production use.
        - Keep output concise and parseable.
        - Add tests for validation and failure paths.
        """
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scaffold a CrewAI custom tool")
    parser.add_argument("name", help="Tool identifier, e.g. weather_lookup")
    parser.add_argument(
        "--path",
        default=".",
        help="Output parent directory (default: current directory)",
    )
    parser.add_argument(
        "--style",
        choices=["basetool", "decorator"],
        default="basetool",
        help="Tool implementation style",
    )
    parser.add_argument(
        "--description",
        default="TODO: describe what this tool does and when to use it.",
        help="Human-readable tool description",
    )
    parser.add_argument(
        "--env-var",
        action="append",
        default=[],
        help="Required environment variable; repeat for multiple entries",
    )
    parser.add_argument(
        "--dependency",
        action="append",
        default=[],
        help="Package dependency; repeat for multiple entries",
    )
    parser.add_argument(
        "--with-async",
        action="store_true",
        help="Add async implementation scaffold",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files in target folder",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        base_identifier = normalize_identifier(args.name)
    except ValueError as exc:
        print(f"Error: {exc}")
        return 1

    module_name = ensure_suffix(base_identifier, "_tool")
    output_dir = Path(args.path).resolve() / module_name
    code_path = output_dir / f"{module_name}.py"
    readme_path = output_dir / "README.md"

    if output_dir.exists() and not args.force:
        print(f"Error: output directory already exists: {output_dir}")
        print("Pass --force to overwrite files.")
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    if args.style == "basetool":
        class_name = snake_to_camel(module_name)
        schema_name = class_name + "Input"
        display_name = camel_to_words(class_name)
        code = render_basetool(
            class_name=class_name,
            schema_name=schema_name,
            display_name=display_name,
            description=args.description,
            env_vars=args.env_var,
            dependencies=args.dependency,
            with_async=args.with_async,
        )
        identity = class_name
    else:
        function_name = module_name
        display_name = camel_to_words(snake_to_camel(module_name))
        code = render_decorator(
            function_name=function_name,
            display_name=display_name,
            description=args.description,
            with_async=args.with_async,
        )
        identity = function_name

    readme = render_readme(
        class_or_function_name=identity,
        style=args.style,
        env_vars=args.env_var,
        dependencies=args.dependency,
    )

    code_path.write_text(code)
    readme_path.write_text(readme)

    print("Created custom tool scaffold:")
    print(f"- {code_path}")
    print(f"- {readme_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
