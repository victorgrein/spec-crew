#!/usr/bin/env python3
"""
Basic Flow Template - Simple @start and @listen decorators.

This template demonstrates:
- Minimal structured state with Pydantic
- Sequential flow execution
- Basic @start and @listen decorators
- State passing between steps
"""

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel


class SimpleState(BaseModel):
    """Minimal state definition."""

    message: str = ""
    counter: int = 0


class BasicFlow(Flow[SimpleState]):
    """
    Simple flow demonstrating basic decorators.

    Execution: init -> process -> finalize
    """

    @start()
    def init(self):
        """
        First step - entry point.

        @start() marks this as the flow entry point.
        """
        print("Step 1: Initialization")
        self.state.message = "Hello from flow"
        self.state.counter = 1
        return self.state.message

    @listen(init)
    def process(self, previous_result):
        """
        Second step - listens to init.

        @listen(init) runs after init() completes.
        Receives the return value from init().
        """
        print(f"Step 2: Processing - received: {previous_result}")
        self.state.counter += 1
        return f"Processed: {self.state.message}"

    @listen(process)
    def finalize(self, previous_result):
        """
        Final step - listens to process.

        @listen(process) runs after process() completes.
        """
        print(f"Step 3: Finalizing - received: {previous_result}")
        self.state.counter += 1
        return f"Final result: Counter={self.state.counter}"


def kickoff():
    """Run the flow."""
    flow = BasicFlow()
    result = flow.kickoff()
    print(f"\nFlow completed: {result}")
    print(f"Final state: {flow.state}")


if __name__ == "__main__":
    kickoff()
