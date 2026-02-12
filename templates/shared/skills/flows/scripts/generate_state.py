#!/usr/bin/env python3
"""Generate Pydantic state model interactively."""

import argparse
import sys
from pathlib import Path


VALID_TYPES = {
    "str": "str",
    "string": "str",
    "int": "int",
    "integer": "int",
    "float": "float",
    "double": "float",
    "bool": "bool",
    "boolean": "bool",
    "list": "list",
    "array": "list",
    "dict": "dict",
    "dictionary": "dict",
    "object": "dict",
}


def get_type_annotation(field_type: str, is_optional: bool = False) -> str:
    """Get Python type annotation for field."""
    base_type = VALID_TYPES.get(field_type.lower(), "Any")

    if is_optional:
        return f"Optional[{base_type}]"
    return base_type


def get_default_value(field_type: str, user_default: str | None) -> str | None:
    """Get default value for field."""
    if user_default is None:
        return None

    user_default = user_default.strip()

    if not user_default or user_default.lower() == "none":
        return None

    type_lower = field_type.lower()

    if type_lower in ("str", "string"):
        return f"'{user_default}'"
    elif type_lower in ("int", "integer"):
        try:
            return str(int(user_default))
        except ValueError:
            return None
    elif type_lower in ("float", "double"):
        try:
            return str(float(user_default))
        except ValueError:
            return None
    elif type_lower in ("bool", "boolean"):
        if user_default.lower() in ("true", "yes", "1"):
            return "True"
        elif user_default.lower() in ("false", "no", "0"):
            return "False"
        return None
    elif type_lower in ("list", "array"):
        if user_default.startswith("[") and user_default.endswith("]"):
            return user_default
        return None
    elif type_lower in ("dict", "dictionary", "object"):
        if user_default.startswith("{") and user_default.endswith("}"):
            return user_default
        return None

    return None


def prompt_field() -> dict | None:
    """Prompt user for a field definition."""
    print("\n" + "-" * 40)
    name = input("Field name (or 'done' to finish): ").strip()

    if name.lower() == "done":
        return None

    if not name or not name.replace("_", "").isalnum():
        print("Error: Field name must be alphanumeric with underscores")
        return prompt_field()

    print(f"Available types: {', '.join(sorted(set(VALID_TYPES.keys())))}")
    field_type = input("Field type [str]: ").strip() or "str"

    if field_type.lower() not in VALID_TYPES:
        print(f"Warning: Unknown type '{field_type}', using 'Any'")

    is_optional = input("Optional? [y/N]: ").strip().lower() == "y"

    default_prompt = "Leave empty for no default"
    if field_type.lower() in ("str", "string"):
        default_prompt = "Leave empty for no default"
    elif field_type.lower() in ("bool", "boolean"):
        default_prompt = "true/false or leave empty"

    default = input(f"Default value ({default_prompt}): ").strip()
    default = default if default else None

    description = input("Field description (optional): ").strip()

    return {
        "name": name,
        "type": field_type,
        "optional": is_optional,
        "default": default,
        "description": description,
    }


def generate_model_code(class_name: str, fields: list) -> str:
    """Generate Pydantic model code."""
    lines = [
        "#!/usr/bin/env python3",
        '"""State model for flow."""',
        "",
        "from pydantic import BaseModel, Field",
        "from typing import Optional",
        "",
        "",
        f"class {class_name}(BaseModel):",
        '    """Structured state for the flow."""',
        "",
    ]

    for field in fields:
        name = field["name"]
        type_annotation = get_type_annotation(field["type"], field["optional"])
        default = get_default_value(field["type"], field["default"])
        description = field["description"]

        # Build field definition
        if default is not None:
            field_def = f"    {name}: {type_annotation} = {default}"
        elif field["optional"]:
            field_def = f"    {name}: {type_annotation} = None"
        else:
            field_def = f"    {name}: {type_annotation}"

        # Add Field() for description
        if description:
            if "=" in field_def:
                field_def = field_def.replace(
                    " = ",
                    f' = Field(default={default}, description="{description}")  # type: ignore\n    # Original: ',
                )
                # Actually, let's do it cleaner
                field_def = f'    {name}: {type_annotation} = Field(default={default}, description="{description}")'
            else:
                field_def = f'    {name}: {type_annotation} = Field(description="{description}")'

        lines.append(field_def)

    if not fields:
        lines.append("    pass")

    lines.append("")
    lines.append("    class Config:")
    lines.append('        """Pydantic config."""')
    lines.append("        arbitrary_types_allowed = True")
    lines.append("")

    return "\n".join(lines)


def generate_state(output_file: str | Path, class_name: str | None = None) -> Path:
    """Interactive state model generation.

    Args:
        output_file: Path to save the generated model
        class_name: Name for the state class (default: FlowState)

    Returns:
        Path to generated file
    """
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if class_name is None:
        class_name = input("Class name [FlowState]: ").strip() or "FlowState"

    print(f"\n📝 Defining fields for '{class_name}'")
    print("Enter 'done' as field name when finished")

    fields = []
    while True:
        field = prompt_field()
        if field is None:
            break
        fields.append(field)
        print(f"✓ Added field: {field['name']} ({field['type']})")

    if not fields:
        print("Warning: No fields defined. Creating empty model.")

    # Generate code
    code = generate_model_code(class_name, fields)

    # Write file
    output_file.write_text(code)

    print(f"\n✓ State model generated: {output_file}")
    print(f"  Fields: {len(fields)}")

    return output_file


def main():
    """CLI interface for state model generation."""
    parser = argparse.ArgumentParser(
        description="Generate Pydantic state model interactively",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  generate_state.py --output state.py
  generate_state.py --output state.py --class-name MyFlowState
        """,
    )
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    parser.add_argument("--class-name", help="State class name (default: FlowState)")

    args = parser.parse_args()

    try:
        generate_state(args.output, args.class_name)
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
