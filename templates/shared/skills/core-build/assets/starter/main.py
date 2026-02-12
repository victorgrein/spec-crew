#!/usr/bin/env python3
"""Entry point for {CrewName} crew."""

import sys
from crew import {CrewName}Crew

def main():
    """Run the crew with CLI inputs."""
    if len(sys.argv) < 2:
        print("Usage: python main.py '<topic>'")
        print("Example: python main.py 'artificial intelligence'")
        sys.exit(1)
    
    topic = sys.argv[1]
    inputs = {"topic": topic}
    
    print(f"Starting research on: {topic}")
    print("=" * 50)
    
    result = {CrewName}Crew().crew().kickoff(inputs=inputs)
    
    print("\n" + "=" * 50)
    print("CREW EXECUTION COMPLETE")
    print(result)

if __name__ == "__main__":
    main()
