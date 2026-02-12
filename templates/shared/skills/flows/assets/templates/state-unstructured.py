#!/usr/bin/env python3
"""
Unstructured State Template - Dictionary-based state.

This template demonstrates:
- Dictionary-like state access
- Dynamic key-value pairs
- Flexible state structure
- Use cases where schema is not fixed
"""

from crewai.flow.flow import Flow, listen, start


class UnstructuredStateFlow(Flow):
    """
    Flow using unstructured (dictionary) state.

    Benefits:
    - Flexibility - add/remove keys dynamically
    - Simplicity - no schema definition needed
    - Good for prototyping

    Trade-offs:
    - No type checking
    - No IDE autocompletion
    - Potential runtime errors
    """

    @start()
    def initialize(self):
        """
        Initialize with dynamic keys.

        With unstructured state, you can add any key dynamically.
        """
        print("Initializing with unstructured state...")

        # Add arbitrary keys
        self.state["request_id"] = "req-456"
        self.state["user"] = {"name": "Jane Doe", "email": "jane@example.com"}
        self.state["items"] = ["a", "b", "c"]
        self.state["metadata"] = {"source": "api", "version": "1.0"}

        # Access the automatic flow ID
        print(f"Flow ID: {self.state['id']}")

        return "initialized"

    @listen(initialize)
    def process(self, _):
        """Process and add more dynamic fields."""
        print("Processing with dynamic state...")

        # Access nested data
        user_name = self.state["user"]["name"]
        print(f"Processing for user: {user_name}")

        # Add new fields on the fly
        self.state["processed_at"] = "2024-01-01T00:00:00"
        self.state["results"] = []

        # Modify existing data
        for item in self.state["items"]:
            self.state["results"].append(f"result_{item}")

        # Add computed fields
        self.state["total_items"] = len(self.state["items"])
        self.state["success"] = True

        return "processed"

    @listen(process)
    def finalize(self, _):
        """Complete and display state."""
        print("\nUnstructured state contents:")
        for key, value in self.state.items():
            if key != "id":  # Skip the auto-generated ID
                print(f"  {key}: {value}")

        return "completed"


def kickoff():
    """Run the unstructured state flow."""
    flow = UnstructuredStateFlow()
    result = flow.kickoff()
    print(f"\nFinal result: {result}")


if __name__ == "__main__":
    kickoff()
