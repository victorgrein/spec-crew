#!/usr/bin/env python3
"""Validate CrewAI Flow structure."""

import ast
import sys
from pathlib import Path


def find_class_with_decorator(node: ast.ClassDef, decorator_name: str) -> bool:
    """Check if a class has a specific decorator."""
    for decorator in node.decorators:
        if isinstance(decorator, ast.Name) and decorator.id == decorator_name:
            return True
        if isinstance(decorator, ast.Attribute) and decorator.attr == decorator_name:
            return True
    return False


def get_decorator_names(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list:
    """Extract decorator names from a function."""
    names = []
    for decorator in node.decorators:
        if isinstance(decorator, ast.Name):
            names.append(decorator.id)
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                names.append(decorator.func.id)
            elif isinstance(decorator.func, ast.Attribute):
                names.append(decorator.func.attr)
        elif isinstance(decorator, ast.Attribute):
            names.append(decorator.attr)
    return names


def get_router_labels(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list:
    """Extract router labels from @router decorator."""
    labels = []
    for decorator in node.decorators:
        if isinstance(decorator, ast.Call):
            func_name = None
            if isinstance(decorator.func, ast.Name):
                func_name = decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                func_name = decorator.func.attr

            if func_name == "router":
                # Check for keyword arguments (e.g., router(labels=[...]))
                for keyword in decorator.keywords:
                    if keyword.arg == "labels" and isinstance(keyword.value, ast.List):
                        for elt in keyword.value.elts:
                            if isinstance(elt, ast.Constant):
                                labels.append(elt.value)
    return labels


def validate_flow(file_path: str | Path) -> list:
    """Check flow for common issues.

    Args:
        file_path: Path to the flow file

    Returns:
        List of error messages
    """
    errors = []
    file_path = Path(file_path)

    if not file_path.exists():
        return [f"File not found: {file_path}"]

    try:
        content = file_path.read_text()
        tree = ast.parse(content)
    except SyntaxError as e:
        return [f"Syntax error in {file_path}: {e}"]
    except Exception as e:
        return [f"Error parsing {file_path}: {e}"]

    flow_classes = []
    all_methods = []

    for node in ast.walk(tree):
        # Find Flow classes
        if isinstance(node, ast.ClassDef):
            # Check if it inherits from Flow
            inherits_flow = False
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "Flow":
                    inherits_flow = True
                elif isinstance(base, ast.Attribute) and base.attr == "Flow":
                    inherits_flow = True

            if inherits_flow:
                flow_classes.append(node)

                # Collect all methods in this class
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        all_methods.append(item)

    if not flow_classes:
        errors.append("No Flow class found. Class must inherit from 'Flow'")
        return errors

    if len(flow_classes) > 1:
        errors.append(f"Multiple Flow classes found: {[c.name for c in flow_classes]}")

    for flow_class in flow_classes:
        # Check for @start decorator
        has_start = False
        start_methods = []
        listen_targets = set()
        router_labels = set()
        method_names = set()

        for method in all_methods:
            if method.name.startswith("_"):
                continue

            method_names.add(method.name)
            decorators = get_decorator_names(method)

            if "start" in decorators:
                has_start = True
                start_methods.append(method.name)

            if "listen" in decorators:
                # Extract what this method listens to
                for decorator in method.decorators:
                    if isinstance(decorator, ast.Call):
                        func_name = None
                        if isinstance(decorator.func, ast.Name):
                            func_name = decorator.func.id
                        elif isinstance(decorator.func, ast.Attribute):
                            func_name = decorator.func.attr

                        if func_name == "listen":
                            # Check arguments
                            for arg in decorator.args:
                                if isinstance(arg, ast.Constant):
                                    listen_targets.add(arg.value)
                                elif isinstance(arg, ast.Name):
                                    listen_targets.add(arg.id)

            if "router" in decorators:
                labels = get_router_labels(method)
                router_labels.update(labels)

        if not has_start:
            errors.append(f"Flow class '{flow_class.name}' has no @start method")

        # Check router labels have matching listeners
        for label in router_labels:
            if label not in method_names:
                errors.append(f"Router label '{label}' has no matching @listen handler")

        # Check for state model
        for node in ast.walk(flow_class):
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                if node.target.id == "_state":
                    # Check if it's a Pydantic model reference
                    if isinstance(node.annotation, ast.Name):
                        errors.append(
                            f"State model '{node.annotation.id}' detected - ensure it's a valid Pydantic model"
                        )

    return errors


def main():
    """CLI interface for flow validation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate CrewAI Flow structure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  validate_flow.py my_flow.py
  validate_flow.py src/flows/*.py
        """,
    )
    parser.add_argument("files", nargs="+", help="Flow file(s) to validate")
    parser.add_argument(
        "--strict", action="store_true", help="Treat warnings as errors"
    )

    args = parser.parse_args()

    total_errors = 0

    for file_path in args.files:
        path = Path(file_path)

        # Handle glob patterns
        if "*" in str(path):
            import glob

            files = glob.glob(str(path))
        else:
            files = [path]

        for f in files:
            f = Path(f)
            print(f"\nValidating: {f}")
            print("-" * 40)

            errors = validate_flow(f)

            if not errors:
                print("✓ Flow is valid!")
            else:
                for error in errors:
                    print(f"✗ {error}")
                    total_errors += 1

    print(f"\n{'=' * 40}")
    if total_errors == 0:
        print("✓ All flows validated successfully!")
        sys.exit(0)
    else:
        print(f"✗ Found {total_errors} issue(s)")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(1)
