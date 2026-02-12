# Flow Control Primitives Guide

Comprehensive guide to control flow patterns in CrewAI Flows with full examples and visual diagrams.

---

## Table of Contents

1. [Sequential Execution](#1-sequential-execution)
2. [Conditional Routing (@router)](#2-conditional-routing-router)
3. [Parallel Execution (and_)](#3-parallel-execution-and_)
4. [Alternative Paths (or_)](#4-alternative-paths-or_)
5. [Human-in-the-Loop](#5-human-in-the-loop)
6. [Multi-Start Flows](#6-multi-start-flows)

---

## 1. Sequential Execution

**Purpose**: Execute steps in a linear chain where each step triggers the next.

**When to Use**:
- Simple workflows with clear ordering
- Data transformation pipelines
- Validation chains
- Report generation

### Code Example

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class SimpleState(BaseModel):
    message: str = ""
    step_count: int = 0

class SequentialFlow(Flow[SimpleState]):
    """
    Sequential flow: start → step1 → step2 → step3
    
    Each @listen decorator chains to the previous step.
    """

    @start()
    def init(self):
        """Entry point - step 1"""
        print("Step 1: Initialize")
        self.state.message = "Started"
        self.state.step_count = 1
        return "init_done"

    @listen(init)
    def process(self, previous_result):
        """Step 2 - listens to init"""
        print(f"Step 2: Processing (received: {previous_result})")
        self.state.message += " → Processed"
        self.state.step_count = 2
        return "process_done"

    @listen(process)
    def finalize(self, previous_result):
        """Step 3 - listens to process"""
        print(f"Step 3: Finalize (received: {previous_result})")
        self.state.message += " → Finalized"
        self.state.step_count = 3
        return "complete"

    @listen(finalize)
    def cleanup(self, _):
        """Step 4 - listens to finalize"""
        print(f"Step 4: Cleanup")
        print(f"Final state: {self.state.message}")
        return "cleaned"
```

### Data Flow Diagram

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
│  init   │────▶│ process  │────▶│ finalize │────▶│ cleanup │
│ @start  │     │ @listen  │     │ @listen  │     │@listen  │
└─────────┘     └──────────┘     └──────────┘     └─────────┘
     │                 │                 │                │
     │                 │                 │                │
  "init_done"    "process_done"    "complete"      "cleaned"
```

### Best Practices

1. **Clear Naming**: Name methods to indicate their position in the chain
2. **State Updates**: Update state incrementally in each step
3. **Return Values**: Return meaningful values for debugging
4. **Single Path**: Keep the chain linear - use routers for branches

### Output

```
Step 1: Initialize
Step 2: Processing (received: init_done)
Step 3: Finalize (received: process_done)
Step 4: Cleanup
Final state: Started → Processed → Finalized
```

---

## 2. Conditional Routing (@router)

**Purpose**: Route execution to different paths based on runtime conditions.

**When to Use**:
- Quality gates
- Validation checks
- Decision trees
- Loop patterns (revision cycles)

### Code Example

```python
from crewai.flow.flow import Flow, listen, start, router
from pydantic import BaseModel
from typing import Literal

class RoutingState(BaseModel):
    score: int = 0
    attempts: int = 0
    max_attempts: int = 3
    status: str = "pending"

class ConditionalFlow(Flow[RoutingState]):
    """
    Conditional routing with quality gate and retry loop.
    
    Flow: init → evaluate → [approved|revision|rejected] → finalize
    """

    @start()
    def init(self):
        """Initialize with sample data"""
        print("\n=== Conditional Routing Demo ===\n")
        self.state.score = 65  # Initial quality score
        print(f"Initial score: {self.state.score}")
        return "initialized"

    @router(init)
    def evaluate_quality(self, _):
        """
        Router - returns label based on score.
        
        Returns one of: "approved", "revision", "rejected"
        """
        print(f"\n[Evaluation] Score: {self.state.score}")
        
        if self.state.score >= 80:
            return "approved"
        elif self.state.score >= 60:
            return "revision"
        else:
            return "rejected"

    @listen("approved")
    def handle_approved(self):
        """Handle approved path"""
        print("✓ Quality approved!")
        self.state.status = "approved"
        return "success"

    @listen("revision")
    def handle_revision(self):
        """
        Handle revision path with loop back to evaluation.
        
        This creates a cycle: evaluate → revision → evaluate
        """
        self.state.attempts += 1
        print(f"⚠ Revision needed (attempt {self.state.attempts})")
        
        # Simulate improvement
        self.state.score += 10
        print(f"  Score improved to: {self.state.score}")
        
        if self.state.attempts < self.state.max_attempts:
            # Loop back to evaluation
            return self.evaluate_quality("")
        else:
            print(f"  Max attempts ({self.state.max_attempts}) reached")
            return "max_retries"

    @listen("rejected")
    def handle_rejected(self):
        """Handle rejected path"""
        print("✗ Quality rejected")
        self.state.status = "rejected"
        return "failed"

    @listen("success", "max_retries", "failed")
    def finalize(self, result):
        """Listen to all terminal paths"""
        print(f"\n=== Final Status: {self.state.status} ===")
        print(f"Final score: {self.state.score}")
        print(f"Attempts: {self.state.attempts}")
        return result
```

### Data Flow Diagram

```
                    ┌───────────────┐
                    │   evaluate    │
                    │   @router     │
                    └───────┬───────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
    score≥80          60≤score<80          score<60
          │                 │                 │
          ▼                 ▼                 ▼
   ┌────────────┐    ┌────────────┐    ┌────────────┐
   │  approved  │    │  revision  │    │  rejected  │
   │  @listen   │    │  @listen   │    │  @listen   │
   └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
         │                 │                 │
         │                 │ (loop back)     │
         │                 │                 │
         └─────────────────┴─────────────────┘
                           │
                           ▼
                    ┌────────────┐
                    │  finalize  │
                    │  @listen   │
                    └────────────┘
```

### Loop Pattern (Revision Cycle)

```
┌────────────────────────────────────────────────────────────┐
│                     REVISION LOOP                           │
│                                                             │
│   ┌──────────┐      score<80      ┌──────────┐             │
│   │ evaluate │────────────────────▶│ revision │             │
│   │ @router  │                     │ @listen  │             │
│   └────┬─────┘                     └────┬─────┘             │
│        │                                 │                   │
│        │ score≥80                        │ +10 score         │
│        ▼                                 │                   │
│   ┌──────────┐                           │ (loop back)       │
│   │ approved │◀──────────────────────────┘                   │
│   │ @listen  │                                               │
│   └──────────┘                                               │
└────────────────────────────────────────────────────────────┘
```

### Best Practices

1. **Exhaustive Labels**: Ensure all router return values have listeners
2. **Deterministic Routing**: Router should always return valid labels
3. **Loop Protection**: Add attempt counters to prevent infinite loops
4. **Clear Transitions**: Document what each label means

### Output

```
=== Conditional Routing Demo ===

Initial score: 65

[Evaluation] Score: 65
⚠ Revision needed (attempt 1)
  Score improved to: 75

[Evaluation] Score: 75
⚠ Revision needed (attempt 2)
  Score improved to: 85

[Evaluation] Score: 85
✓ Quality approved!

=== Final Status: approved ===
Final score: 85
Attempts: 2
```

---

## 3. Parallel Execution (and_)

**Purpose**: Execute multiple branches simultaneously and wait for all to complete.

**When to Use**:
- Independent operations that can run in parallel
- Fan-in patterns (gathering results from multiple sources)
- Parallel data fetching
- Concurrent processing

### Code Example

```python
from crewai.flow.flow import Flow, listen, start, and_
from pydantic import BaseModel
from typing import List
import time

class ParallelState(BaseModel):
    branch_a_result: str = ""
    branch_b_result: str = ""
    branch_c_result: str = ""
    merged_result: str = ""
    execution_order: List[str] = []

class ParallelFlow(Flow[ParallelState]):
    """
    Parallel execution with and_() for fan-in.
    
    Flow: start → [parallel branches A, B, C] → merge (all must complete)
    """

    @start()
    def init(self):
        """Trigger parallel branches"""
        print("\n=== Parallel Execution Demo ===\n")
        print("Starting parallel branches...")
        return "trigger"

    @listen(init)
    def branch_a(self, _):
        """Branch A - independent work"""
        time.sleep(0.3)  # Simulate work
        self.state.branch_a_result = "Result from Branch A"
        self.state.execution_order.append("A")
        print("✓ Branch A complete")
        return "a_done"

    @listen(init)
    def branch_b(self, _):
        """Branch B - independent work"""
        time.sleep(0.1)  # Simulate work (completes first)
        self.state.branch_b_result = "Result from Branch B"
        self.state.execution_order.append("B")
        print("✓ Branch B complete")
        return "b_done"

    @listen(init)
    def branch_c(self, _):
        """Branch C - independent work"""
        time.sleep(0.5)  # Simulate work (completes last)
        self.state.branch_c_result = "Result from Branch C"
        self.state.execution_order.append("C")
        print("✓ Branch C complete")
        return "c_done"

    @listen(and_(branch_a, branch_b, branch_c))
    def merge_results(self, _):
        """
        Join pattern - runs only when ALL branches complete.
        
        and_() creates a fan-in: waits for A AND B AND C
        """
        print("\n=== All Branches Complete ===")
        print(f"Execution order: {' → '.join(self.state.execution_order)}")
        
        # Merge results from all branches
        self.state.merged_result = (
            f"{self.state.branch_a_result} | "
            f"{self.state.branch_b_result} | "
            f"{self.state.branch_c_result}"
        )
        
        print(f"\nMerged result:")
        print(f"  A: {self.state.branch_a_result}")
        print(f"  B: {self.state.branch_b_result}")
        print(f"  C: {self.state.branch_c_result}")
        
        return "merged"
```

### Data Flow Diagram

```
                         PARALLEL EXECUTION (Fan-Out → Fan-In)

                              ┌─────────┐
                              │  init   │
                              │ @start  │
                              └────┬────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
             ┌──────────┐   ┌──────────┐   ┌──────────┐
             │ branch_a │   │ branch_b │   │ branch_c │
             │ @listen  │   │ @listen  │   │ @listen  │
             │(0.3s)    │   │(0.1s)    │   │(0.5s)    │
             └────┬─────┘   └────┬─────┘   └────┬─────┘
                  │              │              │
                  │              │              │
                  └──────────────┼──────────────┘
                                 │
                                 ▼
                         ┌──────────────┐
                         │  and_(A,B,C) │
                         │   FAN-IN     │
                         └──────┬───────┘
                                │
                                ▼
                         ┌──────────────┐
                         │ merge_results│
                         │   @listen    │
                         └──────────────┘
```

### Timing Diagram

```
Time:    0ms    100ms   300ms   500ms
         │       │       │       │
Branch A │███████████████│       │  (completes at 300ms)
Branch B │███████│       │       │  (completes at 100ms)
Branch C │███████████████████████│  (completes at 500ms)
         │       │       │       │
Merge    │       │       │       │████████
         │       │       │       │       ▲
         │       │       │       │       │
                               and_() triggers here
                               (when ALL complete)
```

### Best Practices

1. **True Independence**: Branches should not depend on each other's state
2. **State Isolation**: Each branch updates its own state fields
3. **and_() Fan-In**: Use and_() to wait for all parallel branches
4. **Merge Results**: Join step combines results from all branches

### Output

```
=== Parallel Execution Demo ===

Starting parallel branches...
✓ Branch B complete
✓ Branch A complete
✓ Branch C complete

=== All Branches Complete ===
Execution order: B → A → C

Merged result:
  A: Result from Branch A
  B: Result from Branch B
  C: Result from Branch C
```

---

## 4. Alternative Paths (or_)

**Purpose**: Execute when ANY of multiple conditions complete (first-wins scenario).

**When to Use**:
- Race conditions (first response wins)
- Multiple data sources (use first available)
- Timeout patterns
- Redundant operations

### Code Example

```python
from crewai.flow.flow import Flow, listen, start, or_
from pydantic import BaseModel
import time
import random

class AlternativeState(BaseModel):
    primary_result: str = ""
    backup_result: str = ""
    used_source: str = ""
    response_times: dict = {}

class AlternativeFlow(Flow[AlternativeState]):
    """
    Alternative paths with or_() for first-completed-wins.
    
    Flow: start → [primary_source, backup_source] → process_first_response
    or_() triggers when EITHER completes first.
    """

    @start()
    def init(self):
        """Trigger both sources"""
        print("\n=== Alternative Paths Demo ===\n")
        print("Querying multiple sources...")
        return "query"

    @listen(init)
    def primary_source(self, _):
        """Primary data source"""
        start_time = time.time()
        
        # Simulate variable response time
        delay = random.uniform(0.5, 1.5)
        time.sleep(delay)
        
        elapsed = time.time() - start_time
        self.state.response_times["primary"] = elapsed
        self.state.primary_result = "Data from PRIMARY source"
        
        print(f"✓ Primary source responded in {elapsed:.2f}s")
        return "primary"

    @listen(init)
    def backup_source(self, _):
        """Backup data source"""
        start_time = time.time()
        
        # Simulate variable response time
        delay = random.uniform(0.3, 1.0)
        time.sleep(delay)
        
        elapsed = time.time() - start_time
        self.state.response_times["backup"] = elapsed
        self.state.backup_result = "Data from BACKUP source"
        
        print(f"✓ Backup source responded in {elapsed:.2f}s")
        return "backup"

    @listen(or_(primary_source, backup_source))
    def process_first_response(self, winner):
        """
        First-wins pattern - runs when EITHER source responds.
        
        or_() triggers when primary OR backup completes first.
        """
        print(f"\n=== First Response Received ===")
        print(f"Winner: {winner}")
        
        if winner == "primary":
            self.state.used_source = "primary"
            data = self.state.primary_result
        else:
            self.state.used_source = "backup"
            data = self.state.backup_result
        
        print(f"Using data from: {self.state.used_source.upper()}")
        print(f"Data: {data}")
        
        # Continue processing with the first response
        return f"processed_{winner}"

    @listen(primary_source, backup_source)
    def log_all_responses(self, source):
        """
        This runs for BOTH responses (not or_).
        
        Useful for logging, metrics, or cleanup.
        """
        print(f"  [Log] {source} completed")
        return source

    @listen(log_all_responses)
    def finalize(self, _):
        """Final step after all logging"""
        print(f"\n=== Summary ===")
        print(f"Primary time: {self.state.response_times.get('primary', 'N/A')}")
        print(f"Backup time: {self.state.response_times.get('backup', 'N/A')}")
        print(f"Used: {self.state.used_source}")
```

### Data Flow Diagram

```
                    ALTERNATIVE PATHS (First-Wins)

                         ┌─────────┐
                         │  init   │
                         │ @start  │
                         └────┬────┘
                              │
              ┌───────────────┴───────────────┐
              │                               │
              ▼                               ▼
       ┌──────────────┐              ┌──────────────┐
       │primary_source│              │ backup_source│
       │ @listen      │              │ @listen      │
       │ (0.5-1.5s)   │              │ (0.3-1.0s)   │
       └──────┬───────┘              └──────┬───────┘
              │                             │
              │                             │
              └───────────┬─────────────────┘
                          │
                   ┌──────▼───────┐
                   │ or_(primary,  │
                   │    backup)   │
                   └──────┬───────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
    ┌───────────────────┐   ┌───────────────────┐
    │process_first_resp │   │  log_all_resp     │
    │  (runs once)      │   │  (runs twice)     │
    └───────────────────┘   └───────────────────┘
```

### Race Condition Pattern

```
Scenario: Primary responds in 0.8s, Backup responds in 0.5s

Time (s):   0    0.5    0.8    1.0
            │     │      │      │
Primary    │████████████│      │  (completes at 0.8s)
            │     │      │      │
Backup     │█████│      │      │  (completes at 0.5s ← FIRST!)
            │     │      │      │
            │     ▼      │      │
            │  or_()     │      │
            │  triggers  │      │
            │     │      │      │
Process    │     │███████│      │  (process_first_response runs)
            │     │      │      │

Result: Backup wins (0.5s < 0.8s)
```

### Best Practices

1. **Race Handling**: Use or_() when you need the fastest response
2. **Logging Separately**: Log all completions with separate @listen
3. **Idempotent Results**: Ensure both paths produce compatible results
4. **Timeout Consideration**: or_() doesn't timeout - use with care

### Output

```
=== Alternative Paths Demo ===

Querying multiple sources...
✓ Backup source responded in 0.45s

=== First Response Received ===
Winner: backup
Using data from: BACKUP
Data: Data from BACKUP source
  [Log] backup completed
✓ Primary source responded in 0.82s
  [Log] primary completed

=== Summary ===
Primary time: 0.82
Backup time: 0.45
Used: backup
```

---

## 5. Human-in-the-Loop

**Purpose**: Pause flow execution for human input, with state persistence during wait.

**When to Use**:
- Approval workflows
- Data validation requiring human judgment
- Complex decision points
- Quality assurance gates

### Code Example

```python
from crewai.flow.flow import Flow, listen, start
from crewai.flow.persistence import persist
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import time

class HumanLoopState(BaseModel):
    pending_approval: bool = False
    approval_requested_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    approval_notes: str = ""
    document_content: str = ""
    approval_status: str = "pending"  # pending, approved, rejected

@persist()
class HumanInTheLoopFlow(Flow[HumanLoopState]):
    """
    Human-in-the-loop pattern with state persistence.
    
    Flow: generate → await_approval → (human approves) → finalize
    
    The @persist decorator ensures state is saved during the wait.
    """

    @start()
    def generate_document(self):
        """Generate content requiring human approval"""
        print("\n=== Human-in-the-Loop Demo ===\n")
        print("Step 1: Generating document...")
        
        self.state.document_content = """
        QUARTERLY REPORT - Q1 2024
        ===========================
        Revenue: $1.2M (+15% YoY)
        Expenses: $800K (+5% YoY)
        Net Profit: $400K
        
        Recommendations:
        1. Increase marketing budget by 20%
        2. Hire 3 additional sales staff
        3. Expand to European markets
        """
        
        print("✓ Document generated")
        return "document_ready"

    @listen(generate_document)
    def request_approval(self, _):
        """
        Request human approval.
        
        In production, this would:
        - Send notification to approver
        - Create approval ticket
        - Wait for external trigger
        """
        self.state.pending_approval = True
        self.state.approval_requested_at = datetime.now()
        
        print("\nStep 2: Approval Requested")
        print(f"  Timestamp: {self.state.approval_requested_at}")
        print(f"  Content: {self.state.document_content[:100]}...")
        
        # Simulate waiting for human input
        # In production, this would block until human responds
        print("\n  [Simulating human approval...]")
        time.sleep(2)  # Simulate wait time
        
        # Simulate human approval (in production, from external trigger)
        return self._simulate_human_approval()

    def _simulate_human_approval(self):
        """Simulate human approval input"""
        self.state.approved_by = "manager@company.com"
        self.state.approval_notes = "Approved with minor revisions needed"
        self.state.approval_status = "approved"
        self.state.pending_approval = False
        
        print(f"\n  ✓ Approved by: {self.state.approved_by}")
        print(f"  Notes: {self.state.approval_notes}")
        
        return "approved"

    @listen(request_approval)
    def finalize_approved(self, _):
        """Process approved document"""
        print("\nStep 3: Processing approved document")
        print(f"  Status: {self.state.approval_status}")
        print(f"  Approved at: {datetime.now()}")
        print(f"  By: {self.state.approved_by}")
        
        # Continue with approved content
        return "published"
```

### Production Implementation

```python
"""
Production Human-in-the-Loop Pattern

In production, replace _simulate_human_approval with:
1. External approval system integration
2. Webhook or message queue listener
3. Resume flow when approval received
"""

from crewai.flow.flow import Flow, listen, start
from crewai.flow.persistence import persist
import asyncio

@persist()
class ProductionHumanLoopFlow(Flow):
    """
    Production-ready human-in-the-loop with external approval.
    """

    @start()
    def init(self):
        """Initialize approval request"""
        self.state.approval_ticket_id = self._create_approval_ticket()
        return self.state.approval_ticket_id

    @listen(init)
    async def await_approval(self, ticket_id):
        """
        Wait for external approval signal.
        
        State is persisted automatically by @persist decorator.
        """
        print(f"Waiting for approval on ticket: {ticket_id}")
        
        # Wait for approval webhook/notification
        approval = await self._wait_for_approval(ticket_id)
        
        return approval

    async def _wait_for_approval(self, ticket_id: str):
        """
        Production: Listen for approval webhook or message.
        """
        # Option 1: Webhook handler
        # Option 2: Message queue listener
        # Option 3: Poll approval API
        
        # Example with asyncio (simplified)
        while True:
            status = await self._check_approval_status(ticket_id)
            if status in ["approved", "rejected"]:
                return status
            await asyncio.sleep(5)  # Poll every 5 seconds

    async def _check_approval_status(self, ticket_id: str):
        """Check approval system for status update."""
        # Call external approval API
        pass
```

### Data Flow Diagram

```
              HUMAN-IN-THE-LOOP PATTERN

  ┌─────────────┐
  │   @start    │
  │  generate   │
  └──────┬──────┘
         │
         ▼
  ┌─────────────┐
  │   @listen   │
  │   request   │
  │  approval   │
  └──────┬──────┘
         │
         │  [Send notification]
         │  [Persist state @persist]
         │
         ▼
  ┌─────────────┐
  │   AWAIT     │
  │   HUMAN     │◄──────────────────┐
  │   INPUT     │                   │
  └─────────────┘                   │
         │                          │
         │                          │
    [State persisted]               │
    [Flow suspended]                │
                                    │
                                    │
                              [Human reviews]
                              [Approves/Rejects]
                                    │
                                    │
         │                          │
         ▼                          │
  ┌─────────────┐                   │
  │   @listen   │───────────────────┘
  │   finalize  │
  └─────────────┘
```

### Resume Pattern

```python
"""
Resuming a paused flow after human input.
"""

# After human approval received:
flow = ProductionHumanLoopFlow()
flow.load_state(flow_id)  # Restore persisted state
result = flow.kickoff()   # Continue from where it left off
```

### Best Practices

1. **@persist Decorator**: Always use for long waits to preserve state
2. **External Triggers**: Use webhooks, queues, or polling for resume
3. **Timeout Handling**: Add max wait time to prevent indefinite blocks
4. **State Documentation**: Track approval metadata (who, when, why)

---

## 6. Multi-Start Flows

**Purpose**: Define multiple entry points with different trigger conditions.

**When to Use**:
- Event-driven flows
- Different initialization paths
- Scheduled vs manual triggers
- Multiple use cases in one flow

### Code Example

```python
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class MultiStartState(BaseModel):
    trigger_type: str = ""
    triggered_at: datetime = None
    source: str = ""
    data: dict = {}

class MultiStartFlow(Flow[MultiStartState]):
    """
    Multiple @start points for different triggers.
    
    Entry points:
    1. manual_trigger - User-initiated
    2. scheduled_trigger - Cron/timer initiated
    3. webhook_trigger - External system initiated
    """

    @start()
    def manual_trigger(self):
        """
        Entry point 1: Manual user trigger.
        
        Use when: User clicks button, runs CLI command
        """
        print("\n=== Multi-Start Flow Demo ===\n")
        print("[Entry Point: MANUAL]")
        
        self.state.trigger_type = "manual"
        self.state.triggered_at = datetime.now()
        self.state.source = "user_interface"
        self.state.data = {"user_id": "user_123", "action": "run_report"}
        
        print(f"  Triggered by: {self.state.source}")
        print(f"  At: {self.state.triggered_at}")
        
        return "manual_start"

    @start()
    def scheduled_trigger(self):
        """
        Entry point 2: Scheduled/cron trigger.
        
        Use when: Timer expires, cron job, scheduled task
        """
        print("\n=== Multi-Start Flow Demo ===\n")
        print("[Entry Point: SCHEDULED]")
        
        self.state.trigger_type = "scheduled"
        self.state.triggered_at = datetime.now()
        self.state.source = "cron_scheduler"
        self.state.data = {"schedule": "0 9 * * *", "job_name": "daily_sync"}
        
        print(f"  Triggered by: {self.state.source}")
        print(f"  Schedule: {self.state.data['schedule']}")
        
        return "scheduled_start"

    @start()
    def webhook_trigger(self):
        """
        Entry point 3: Webhook/API trigger.
        
        Use when: External system calls webhook
        """
        print("\n=== Multi-Start Flow Demo ===\n")
        print("[Entry Point: WEBHOOK]")
        
        self.state.trigger_type = "webhook"
        self.state.triggered_at = datetime.now()
        self.state.source = "external_api"
        self.state.data = {"webhook_id": "wh_456", "event": "payment_received"}
        
        print(f"  Triggered by: {self.state.source}")
        print(f"  Event: {self.state.data['event']}")
        
        return "webhook_start"

    @listen(manual_trigger, scheduled_trigger, webhook_trigger)
    def process_any_start(self, result):
        """
        Common processing for all entry points.
        
        Listens to ALL @start methods.
        """
        print(f"\n[Common Processing]")
        print(f"  Entry type: {self.state.trigger_type}")
        print(f"  Source: {self.state.source}")
        
        # Route based on trigger type
        if self.state.trigger_type == "manual":
            return self._handle_manual()
        elif self.state.trigger_type == "scheduled":
            return self._handle_scheduled()
        else:
            return self._handle_webhook()

    def _handle_manual(self):
        """Manual trigger specific logic"""
        print("  → Handling manual trigger")
        return "manual_processed"

    def _handle_scheduled(self):
        """Scheduled trigger specific logic"""
        print("  → Handling scheduled trigger")
        return "scheduled_processed"

    def _handle_webhook(self):
        """Webhook trigger specific logic"""
        print("  → Handling webhook trigger")
        return "webhook_processed"

    @listen(process_any_start)
    def finalize(self, result):
        """Final step for all paths"""
        print(f"\n[Finalization]")
        print(f"  Result: {result}")
        print(f"  Flow completed successfully")
        return "complete"
```

### Data Flow Diagram

```
              MULTI-START FLOW

         ┌───────────────────────┐
         │   ENTRY POINTS        │
         └───────────────────────┘
                   │
     ┌─────────────┼─────────────┐
     │             │             │
     ▼             ▼             ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ @start  │   │ @start  │   │ @start  │
│ manual  │   │scheduled│   │ webhook │
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     │             │             │
     └─────────────┼─────────────┘
                   │
                   ▼
          ┌────────────────┐
          │ @listen        │
          │ process_any    │
          └───────┬────────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
┌───────────┐ ┌───────────┐ ┌───────────┐
│_handle_   │ │_handle_   │ │_handle_   │
│ manual()  │ │scheduled()│ │webhook()  │
└─────┬─────┘ └─────┬─────┘ └─────┬─────┘
      │             │             │
      └─────────────┼─────────────┘
                    │
                    ▼
            ┌──────────────┐
            │   finalize   │
            │   @listen    │
            └──────────────┘
```

### Trigger Conditions

```python
"""
Determining which @start to invoke.

In production, use:
1. CLI arguments
2. Environment variables
3. Event payload inspection
4. Explicit method calls
"""

# Example: CLI-based trigger selection
def main():
    import sys
    
    flow = MultiStartFlow()
    
    if len(sys.argv) > 1:
        trigger = sys.argv[1]
        
        if trigger == "manual":
            result = flow.manual_trigger()
        elif trigger == "scheduled":
            result = flow.scheduled_trigger()
        elif trigger == "webhook":
            result = flow.webhook_trigger()
        else:
            print(f"Unknown trigger: {trigger}")
            return
        
        # Continue flow from selected start
        flow.kickoff(inputs={"start_method": trigger})

# Example: Event-based trigger selection
def handle_event(event):
    flow = MultiStartFlow()
    
    if event["type"] == "user_action":
        flow.manual_trigger()
    elif event["type"] == "cron":
        flow.scheduled_trigger()
    elif event["type"] == "webhook":
        flow.webhook_trigger()
    
    flow.kickoff()
```

### Best Practices

1. **Clear Documentation**: Document when to use each @start
2. **Common Listener**: Use a single @listen for all starts when possible
3. **State Initialization**: Ensure all paths initialize state properly
4. **Explicit Routing**: Use clear logic to determine which start to invoke

### Output

```
=== Multi-Start Flow Demo ===

[Entry Point: MANUAL]
  Triggered by: user_interface
  At: 2024-01-15 10:30:45

[Common Processing]
  Entry type: manual
  Source: user_interface
  → Handling manual trigger

[Finalization]
  Result: manual_processed
  Flow completed successfully
```

---

## Summary

| Primitive | Use Case | Key Syntax |
|-----------|----------|------------|
| **Sequential** | Linear chains | `@listen(prev_step)` |
| **@router** | Conditional branching | Return labels, `@listen("label")` |
| **and_()** | Parallel + join | `@listen(and_(a, b, c))` |
| **or_()** | First-wins | `@listen(or_(a, b))` |
| **Human Loop** | Pause for input | `@persist()` + wait pattern |
| **Multi-Start** | Multiple entry points | Multiple `@start()` decorators |

### Control Flow Cheat Sheet

```python
# Sequential
@listen(step_a)
def step_b(self): ...

# Router
@router(step_a)
def decide(self): return "label"

@listen("label")
def handle(self): ...

# Parallel (all must complete)
@listen(and_(branch_a, branch_b))
def merge(self): ...

# Alternative (first completes)
@listen(or_(source_a, source_b))
def process_first(self): ...

# Human pause
@persist()
class MyFlow(Flow): ...

# Multiple starts
@start()
def trigger_a(self): ...

@start()
def trigger_b(self): ...
```

These control primitives provide the building blocks for any flow orchestration pattern you need.
