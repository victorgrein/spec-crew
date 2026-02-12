#!/usr/bin/env python3
"""
Advanced Flow Template - All decorators and patterns.

This template demonstrates:
- @router for conditional branching
- @persist for state persistence
- and_ / or_ for parallel execution
- Multiple start points
- Human feedback gates
"""

from crewai.flow.flow import Flow, listen, router, start, and_, or_
from crewai.flow.persistence import persist
from pydantic import BaseModel
from typing import Literal


class AdvancedState(BaseModel):
    """State with fields for advanced patterns."""

    input_data: str = ""
    quality_score: int = 0
    approved: bool = False
    retry_count: int = 0
    branch_a_result: str = ""
    branch_b_result: str = ""


@persist()
class AdvancedFlow(Flow[AdvancedState]):
    """
    Advanced flow demonstrating all control primitives.

    Patterns:
    1. Conditional routing with @router
    2. State persistence with @persist
    3. Parallel branches with and_
    4. Alternative paths with or_
    """

    @start()
    def initialize(self):
        """Entry point with conditional routing."""
        print("Flow initialized")
        self.state.input_data = "sample data"
        return "initialized"

    @router(initialize)
    def evaluate_quality(self, _):
        """
        Router - returns label for conditional routing.

        Returns one of: "approved", "revision", "rejected"
        """
        # Simulate quality evaluation
        self.state.quality_score = 75

        if self.state.quality_score >= 80:
            return "approved"
        elif self.state.quality_score >= 60:
            return "revision"
        else:
            return "rejected"

    @listen("approved")
    def handle_approval(self):
        """Listen for 'approved' label from router."""
        print("Quality approved!")
        self.state.approved = True
        return "approved"

    @listen("revision")
    def handle_revision(self):
        """Listen for 'revision' label - implements retry loop."""
        self.state.retry_count += 1
        print(f"Revision needed (attempt {self.state.retry_count})")

        if self.state.retry_count < 3:
            # Loop back to evaluation
            return self.evaluate_quality("")
        else:
            return "max_retries_reached"

    @listen("rejected")
    def handle_rejection(self):
        """Listen for 'rejected' label."""
        print("Quality rejected")
        return "rejected"

    @listen(and_(handle_approval, "max_retries_reached"))
    def parallel_branches_trigger(self):
        """
        Trigger parallel branches using and_.

        Runs when both handle_approval AND max_retries_reached complete.
        """
        print("Starting parallel branches")
        return "parallel_start"

    @listen(parallel_branches_trigger)
    def branch_a(self, _):
        """Parallel branch A."""
        print("Branch A executing")
        self.state.branch_a_result = "Result A"
        return "branch_a_done"

    @listen(parallel_branches_trigger)
    def branch_b(self, _):
        """Parallel branch B."""
        print("Branch B executing")
        self.state.branch_b_result = "Result B"
        return "branch_b_done"

    @listen(and_(branch_a, branch_b))
    def merge_branches(self, _):
        """
        Join parallel branches.

        Runs only when both branch_a AND branch_b complete.
        """
        print(f"Merging: {self.state.branch_a_result} + {self.state.branch_b_result}")
        return "merged"

    @listen(or_("approved", "rejected"))
    def alternative_listener(self):
        """
        Alternative path using or_.

        Runs when EITHER approved OR rejected completes.
        """
        print("Alternative path executed")
        return "alternative"

    @listen(merge_branches)
    def finalize(self, _):
        """Final step."""
        print(f"\nFlow completed!")
        print(f"State: {self.state}")
        return "completed"


def kickoff():
    """Run the advanced flow."""
    flow = AdvancedFlow()
    result = flow.kickoff()
    print(f"\nFinal result: {result}")


def plot():
    """Visualize the flow."""
    flow = AdvancedFlow()
    flow.plot("advanced_flow")
    print("Flow visualization saved to advanced_flow.html")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "plot":
        plot()
    else:
        kickoff()
