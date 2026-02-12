#!/usr/bin/env python3
"""Generate flow visualization."""

import argparse
import sys
import os
import importlib.util
import tempfile
import shutil
from pathlib import Path


def plot_flow(file_path: str | Path, output_path: str | Path | None = None) -> Path:
    """Generate HTML visualization of flow.

    Args:
        file_path: Path to the flow file
        output_path: Output file path (default: {flow_name}_plot.html)

    Returns:
        Path to generated visualization file
    """
    file_path = Path(file_path).resolve()

    if not file_path.exists():
        raise FileNotFoundError(f"Flow file not found: {file_path}")

    # Determine output path
    if output_path is None:
        output_path = file_path.parent / f"{file_path.stem}_plot.html"
    else:
        output_path = Path(output_path)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Import the flow module dynamically
    module_name = file_path.stem
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)

    # Add the file's directory to sys.path for imports
    original_path = sys.path.copy()
    sys.path.insert(0, str(file_path.parent))

    try:
        spec.loader.exec_module(module)
    except Exception as e:
        sys.path = original_path
        raise ImportError(f"Failed to import flow module: {e}")
    finally:
        sys.path = original_path

    # Find Flow classes in the module
    flow_classes = []
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, type) and attr_name != "Flow":
            # Check if it's a Flow subclass
            try:
                from crewai.flow import Flow

                if issubclass(attr, Flow) and attr != Flow:
                    flow_classes.append(attr)
            except ImportError:
                pass

    if not flow_classes:
        raise ValueError(f"No Flow class found in {file_path}")

    # Use the first Flow class found
    FlowClass = flow_classes[0]

    # Instantiate the flow
    try:
        flow = FlowClass()
    except Exception as e:
        raise RuntimeError(f"Failed to instantiate flow: {e}")

    # Generate plot
    try:
        plot_result = flow.plot()

        # The plot() method might return the HTML content directly
        # or save it to a file. Let's handle both cases.
        if isinstance(plot_result, str) and plot_result.endswith(".html"):
            # It returned a file path, copy it
            shutil.copy(plot_result, output_path)
        elif plot_result is None:
            # It saved to a default location, try to find it
            default_plot = file_path.parent / f"{FlowClass.__name__}_plot.html"
            if default_plot.exists():
                if output_path != default_plot:
                    shutil.copy(default_plot, output_path)
            else:
                print("Warning: plot() returned None and no default plot found")
        else:
            # Assume it returned HTML content
            output_path.write_text(str(plot_result))

    except Exception as e:
        raise RuntimeError(f"Failed to generate plot: {e}")

    return output_path


def main():
    """CLI interface for flow visualization."""
    parser = argparse.ArgumentParser(
        description="Generate visualization for CrewAI Flows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  plot_flow.py my_flow.py
  plot_flow.py my_flow.py --output flow_diagram.html
        """,
    )
    parser.add_argument("file", help="Path to flow file")
    parser.add_argument(
        "-o", "--output", help="Output file path (default: {flow_name}_plot.html)"
    )
    parser.add_argument(
        "--open",
        action="store_true",
        dest="open_browser",
        help="Open the visualization in browser after generation",
    )

    args = parser.parse_args()

    try:
        output_path = plot_flow(args.file, args.output)
        print(f"✓ Visualization generated: {output_path}")

        if args.open_browser:
            import webbrowser

            webbrowser.open(f"file://{output_path.absolute()}")
            print("  Opening in browser...")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ImportError as e:
        print(f"Import Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error generating visualization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(1)
