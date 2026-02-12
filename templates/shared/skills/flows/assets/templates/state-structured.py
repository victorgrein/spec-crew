#!/usr/bin/env python3
"""
Structured State Template - Pydantic models with type safety.

This template demonstrates:
- Pydantic BaseModel for state definition
- Nested state models
- Type validation
- IDE autocompletion support
"""

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class UserProfile(BaseModel):
    """Nested model for user data."""

    name: str = ""
    email: str = ""
    preferences: dict = Field(default_factory=dict)


class ProcessingResult(BaseModel):
    """Model for processing results."""

    status: str = "pending"
    output: str = ""
    timestamp: datetime = Field(default_factory=datetime.now)


class StructuredState(BaseModel):
    """
    Main state model with type-safe fields.

    Benefits:
    - Type checking at development time
    - Automatic validation
    - Default values
    - IDE autocompletion
    """

    # Basic fields
    request_id: str = Field(default="", description="Unique request identifier")
    user: UserProfile = Field(default_factory=UserProfile)

    # Collections
    items: List[str] = Field(default_factory=list)
    results: List[ProcessingResult] = Field(default_factory=list)

    # Progress tracking
    current_step: int = 0
    total_steps: int = 5
    progress_percentage: float = 0.0

    # Status
    completed: bool = False
    error_message: Optional[str] = None


class StructuredStateFlow(Flow[StructuredState]):
    """
    Flow demonstrating structured state management.
    """

    @start()
    def initialize(self):
        """Initialize state with structured data."""
        print("Initializing with structured state...")

        # Type-safe field access
        self.state.request_id = "req-123"
        self.state.user = UserProfile(
            name="John Doe",
            email="john@example.com",
            preferences={"theme": "dark", "language": "en"},
        )

        # Working with lists
        self.state.items = ["item1", "item2", "item3"]

        self._update_progress()
        return "initialized"

    @listen(initialize)
    def process_items(self, _):
        """Process items and store results."""
        print(f"Processing {len(self.state.items)} items...")

        for item in self.state.items:
            result = ProcessingResult(
                status="completed",
                output=f"Processed: {item}",
                timestamp=datetime.now(),
            )
            self.state.results.append(result)
            print(f"  - {item} -> {result.status}")

        self.state.current_step = 3
        self._update_progress()
        return "processed"

    @listen(process_items)
    def finalize(self, _):
        """Complete the flow."""
        self.state.completed = True
        self.state.current_step = self.state.total_steps
        self._update_progress()

        print(f"\nStructured state benefits:")
        print(
            f"  - Type-safe access: self.state.request_id = '{self.state.request_id}'"
        )
        print(f"  - Nested models: self.state.user.name = '{self.state.user.name}'")
        print(f"  - Collection handling: {len(self.state.results)} results")
        print(f"  - Validation: All fields conform to their types")

        return "completed"

    def _update_progress(self):
        """Helper method to calculate progress."""
        if self.state.total_steps > 0:
            self.state.progress_percentage = (
                self.state.current_step / self.state.total_steps
            ) * 100
        print(f"Progress: {self.state.progress_percentage:.1f}%")


def kickoff():
    """Run the structured state flow."""
    flow = StructuredStateFlow()
    result = flow.kickoff()
    print(f"\nFinal state:\n{flow.state.model_dump_json(indent=2)}")


if __name__ == "__main__":
    kickoff()
