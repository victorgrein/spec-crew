#!/usr/bin/env python3
"""
Guide Creator Flow - Production-ready CrewAI Flow example.

This flow demonstrates:
- Structured state management with Pydantic
- @start and @listen decorators for event-driven control
- Integration with a crew (defined separately using core-build patterns)
- Direct LLM calls for structured outputs
- State persistence with @persist

Prerequisites:
- A crew project created using core-build skill patterns
- Environment variables configured
"""

import json
import os
from typing import List, Dict
from pydantic import BaseModel, Field
from crewai import LLM
from crewai.flow.flow import Flow, listen, start
from crewai.flow.persistence import persist

# Import your crew (created using core-build patterns)
# from crews.content_crew.content_crew import ContentCrew


class Section(BaseModel):
    """Represents a single section in the guide outline."""

    title: str = Field(description="Title of the section")
    description: str = Field(
        description="Brief description of what the section should cover"
    )


class GuideOutline(BaseModel):
    """Structured outline for the guide."""

    title: str = Field(description="Title of the guide")
    introduction: str = Field(description="Introduction to the topic")
    target_audience: str = Field(description="Description of the target audience")
    sections: List[Section] = Field(description="List of sections in the guide")
    conclusion: str = Field(description="Conclusion or summary of the guide")


class GuideCreatorState(BaseModel):
    """Flow state with type-safe fields."""

    topic: str = ""
    audience_level: str = ""
    guide_outline: GuideOutline = None
    sections_content: Dict[str, str] = {}
    completed_sections: List[str] = []
    current_section_index: int = 0


@persist()
class GuideCreatorFlow(Flow[GuideCreatorState]):
    """
    Flow for creating comprehensive learning guides.

    Demonstrates state management, decorator patterns, and crew integration.
    Uses @persist for automatic state persistence between executions.
    """

    @start()
    def get_user_input(self):
        """
        Start the flow by collecting user input.

        State changes:
        - Sets topic and audience_level fields
        """
        print("\n=== Create Your Comprehensive Guide ===\n")

        self.state.topic = input("What topic would you like to create a guide for? ")

        while True:
            audience = input(
                "Who is your target audience? (beginner/intermediate/advanced) "
            ).lower()
            if audience in ["beginner", "intermediate", "advanced"]:
                self.state.audience_level = audience
                break
            print("Please enter 'beginner', 'intermediate', or 'advanced'")

        print(
            f"\nCreating a guide on {self.state.topic} for {self.state.audience_level} audience...\n"
        )
        return self.state

    @listen(get_user_input)
    def create_guide_outline(self, state):
        """
        Create a structured outline using direct LLM call.

        Demonstrates:
        - Structured output with Pydantic models
        - Direct LLM calls for simple tasks
        - State updates with typed data
        """
        print("Creating guide outline...")

        llm = LLM(model="anthropic/claude-sonnet-4-5", response_format=GuideOutline)

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant designed to output JSON.",
            },
            {
                "role": "user",
                "content": f"""
            Create a detailed outline for a comprehensive guide on "{state.topic}" 
            for {state.audience_level} level learners.

            The outline should include:
            1. A compelling title for the guide
            2. An introduction to the topic
            3. 4-6 main sections that cover the most important aspects
            4. A conclusion or summary

            For each section, provide a clear title and a brief description.
            """,
            },
        ]

        response = llm.call(messages=messages)
        outline_dict = json.loads(response)
        self.state.guide_outline = GuideOutline(**outline_dict)

        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)

        with open("output/guide_outline.json", "w") as f:
            json.dump(outline_dict, f, indent=2)

        print(
            f"Guide outline created with {len(self.state.guide_outline.sections)} sections"
        )
        return self.state.guide_outline

    @listen(create_guide_outline)
    def initialize_sections(self, outline):
        """
        Initialize section processing.

        Demonstrates state initialization for iterative processing.
        """
        print("\nStarting section processing...")
        self.state.current_section_index = 0
        self.state.completed_sections = []
        return outline.sections[0] if outline.sections else None

    @listen(initialize_sections)
    def process_section(self, section):
        """
        Process a single section (placeholder for crew integration).

        In production, this would call your crew:
        result = ContentCrew().crew().kickoff(inputs={...})

        Demonstrates:
        - Iterative state updates
        - Progress tracking
        - Conditional flow control
        """
        if section is None:
            return "No sections to process"

        print(f"Processing section: {section.title}")

        # Simulate crew processing
        content = f"## {section.title}\n\n{section.description}\n\n"
        content += "[Content would be generated by your content crew here]\n\n"

        # Update state
        self.state.sections_content[section.title] = content
        self.state.completed_sections.append(section.title)
        self.state.current_section_index += 1

        print(
            f"Completed section {len(self.state.completed_sections)}/{len(self.state.guide_outline.sections)}"
        )

        # Return section to signal completion
        return section

    @listen(process_section)
    def check_completion(self, processed_section):
        """
        Check if all sections are complete.

        Demonstrates conditional flow logic and routing preparation.
        """
        if self.state.current_section_index < len(self.state.guide_outline.sections):
            # More sections to process
            next_section = self.state.guide_outline.sections[
                self.state.current_section_index
            ]
            return {"action": "continue", "section": next_section}
        else:
            # All sections complete
            return {"action": "complete"}

    @listen(check_completion)
    def compile_guide(self, result):
        """
        Compile the final guide.

        Demonstrates aggregation of state data into final output.
        """
        if result.get("action") == "continue":
            # Loop back to process next section
            return self.process_section(result["section"])

        print("\nCompiling final guide...")

        outline = self.state.guide_outline
        guide_content = f"# {outline.title}\n\n"
        guide_content += f"## Introduction\n\n{outline.introduction}\n\n"

        for section in outline.sections:
            section_content = self.state.sections_content.get(section.title, "")
            guide_content += f"\n{section_content}\n"

        guide_content += f"\n## Conclusion\n\n{outline.conclusion}\n\n"

        with open("output/complete_guide.md", "w") as f:
            f.write(guide_content)

        return guide_content

    @listen(compile_guide)
    def finalize(self, content):
        """
        Final step - log completion and return summary.
        """
        print("\n" + "=" * 50)
        print("FLOW EXECUTION COMPLETE")
        print("=" * 50)
        print(f"Flow ID: {self.state.id}")
        print(f"Topic: {self.state.topic}")
        print(f"Sections completed: {len(self.state.completed_sections)}")
        print(f"Output saved to: output/complete_guide.md")
        return content


def kickoff():
    """Entry point to run the flow."""
    flow = GuideCreatorFlow()
    result = flow.kickoff()
    print("\n=== Flow Complete ===")
    return result


def plot():
    """Generate flow visualization."""
    flow = GuideCreatorFlow()
    flow.plot("guide_creator_flow")
    print("Flow visualization saved to guide_creator_flow.html")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "plot":
        plot()
    else:
        kickoff()
