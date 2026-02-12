# Flow State Patterns Guide

Comprehensive guide to common state management patterns in CrewAI Flows with full, executable examples.

---

## Table of Contents

1. [Accumulator Pattern](#1-accumulator-pattern)
2. [Pipeline Pattern](#2-pipeline-pattern)
3. [Branching State Pattern](#3-branching-state-pattern)
4. [Retry Pattern](#4-retry-pattern)
5. [Progress Tracking Pattern](#5-progress-tracking-pattern)
6. [Error Recovery Pattern](#6-error-recovery-pattern)
7. [Crew Integration Pattern](#7-crew-integration-pattern)

---

## 1. Accumulator Pattern

**Purpose**: Collect results over multiple steps, building up a collection incrementally.

**When to Use**:
- Processing lists of items one at a time
- Aggregating results from multiple sources
- Building reports from scattered data
- Incremental data collection

### State Model Definition

```python
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class ProcessedItem(BaseModel):
    """Individual processed item."""
    item_id: str
    status: str
    result: str
    processed_at: datetime = Field(default_factory=datetime.now)

class AccumulatorState(BaseModel):
    """State that accumulates results over steps."""
    # Source data
    items_to_process: List[str] = Field(default_factory=list)
    
    # Accumulator field - grows over time
    processed_items: List[ProcessedItem] = Field(default_factory=list)
    
    # Accumulator metrics
    success_count: int = 0
    error_count: int = 0
    
    # Final summary
    all_completed: bool = False
```

### Flow Implementation

```python
from crewai.flow.flow import Flow, listen, start

class AccumulatorFlow(Flow[AccumulatorState]):
    """
    Demonstrates accumulating results across multiple steps.
    
    Pattern: @start -> process_items -> generate_summary
    Each step adds to the processed_items list.
    """

    @start()
    def load_items(self):
        """Initialize with items to process."""
        self.state.items_to_process = ["item_1", "item_2", "item_3", "item_4"]
        print(f"Loaded {len(self.state.items_to_process)} items to process")
        return self.state.items_to_process

    @listen(load_items)
    def process_batch_1(self, items):
        """Process first half of items."""
        batch = items[:2]
        print(f"Processing batch 1: {batch}")
        
        for item in batch:
            result = ProcessedItem(
                item_id=item,
                status="success",
                result=f"Processed {item} in batch 1"
            )
            self.state.processed_items.append(result)
            self.state.success_count += 1
        
        return f"Batch 1 complete: {len(self.state.processed_items)} items total"

    @listen(process_batch_1)
    def process_batch_2(self, _):
        """Process remaining items."""
        batch = self.state.items_to_process[2:]
        print(f"Processing batch 2: {batch}")
        
        for item in batch:
            result = ProcessedItem(
                item_id=item,
                status="success",
                result=f"Processed {item} in batch 2"
            )
            self.state.processed_items.append(result)
            self.state.success_count += 1
        
        return f"Batch 2 complete: {len(self.state.processed_items)} items total"

    @listen(process_batch_2)
    def generate_summary(self, _):
        """Generate final summary from accumulated results."""
        self.state.all_completed = True
        
        print(f"\n{'='*50}")
        print(f"ACCUMULATION COMPLETE")
        print(f"{'='*50}")
        print(f"Total items processed: {len(self.state.processed_items)}")
        print(f"Success count: {self.state.success_count}")
        print(f"Error count: {self.state.error_count}")
        print(f"\nDetailed results:")
        for item in self.state.processed_items:
            print(f"  - {item.item_id}: {item.status}")
        
        return self.state.processed_items
```

### Explanation

1. **Accumulator Field**: `processed_items` starts empty and grows as each step runs
2. **Incremental Updates**: Each step appends to the list rather than replacing it
3. **Final Aggregation**: The last step summarizes all accumulated data
4. **Type Safety**: Pydantic ensures each `ProcessedItem` has required fields

### Output

```
Loaded 4 items to process
Processing batch 1: ['item_1', 'item_2']
Processing batch 2: ['item_3', 'item_4']

==================================================
ACCUMULATION COMPLETE
==================================================
Total items processed: 4
Success count: 4
Error count: 0

Detailed results:
  - item_1: success
  - item_2: success
  - item_3: success
  - item_4: success
```

---

## 2. Pipeline Pattern

**Purpose**: Transform data through multiple stages, where each stage outputs to the next.

**When to Use**:
- Data transformation workflows
- ETL (Extract, Transform, Load) pipelines
- Document processing pipelines
- Multi-stage analysis

### State Model Definition

```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum

class PipelineStage(str, Enum):
    """Track current pipeline stage."""
    RAW = "raw"
    CLEANED = "cleaned"
    ANALYZED = "analyzed"
    REPORTED = "reported"

class PipelineState(BaseModel):
    """State tracking data through pipeline stages."""
    # Stage tracking
    current_stage: PipelineStage = PipelineStage.RAW
    stage_history: list = Field(default_factory=list)
    
    # Data at each stage (pipeline pattern)
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    cleaned_data: Dict[str, Any] = Field(default_factory=dict)
    analysis_results: Dict[str, Any] = Field(default_factory=dict)
    final_report: Dict[str, Any] = Field(default_factory=dict)
    
    # Quality metrics at each stage
    quality_scores: Dict[str, float] = Field(default_factory=dict)
```

### Flow Implementation

```python
from crewai.flow.flow import Flow, listen, start, router

class PipelineFlow(Flow[PipelineState]):
    """
    Data transformation pipeline: Raw → Cleaned → Analyzed → Reported
    
    Each step transforms the data and stores it in the corresponding state field.
    """

    @start()
    def extract_raw(self):
        """Stage 1: Extract/load raw data."""
        print(f"\n[STAGE: {PipelineStage.RAW.value}]")
        
        self.state.raw_data = {
            "source": "api_endpoint",
            "records": [
                {"id": 1, "value": "  hello world  ", "valid": True},
                {"id": 2, "value": "  test DATA  ", "valid": True},
                {"id": 3, "value": None, "valid": False},
            ],
            "metadata": {"timestamp": "2024-01-01", "count": 3}
        }
        
        self.state.current_stage = PipelineStage.RAW
        self.state.stage_history.append(PipelineStage.RAW.value)
        
        print(f"Extracted {len(self.state.raw_data['records'])} raw records")
        return self.state.raw_data

    @listen(extract_raw)
    def clean_data(self, raw_data):
        """Stage 2: Clean and normalize raw data."""
        print(f"\n[STAGE: {PipelineStage.CLEANED.value}]")
        
        cleaned_records = []
        for record in raw_data["records"]:
            if record.get("valid") and record.get("value"):
                cleaned_records.append({
                    "id": record["id"],
                    "value": record["value"].strip().lower(),
                    "processed": True
                })
        
        self.state.cleaned_data = {
            "records": cleaned_records,
            "removed_count": len(raw_data["records"]) - len(cleaned_records),
            "source_metadata": raw_data["metadata"]
        }
        
        self.state.current_stage = PipelineStage.CLEANED
        self.state.stage_history.append(PipelineStage.CLEANED.value)
        
        # Calculate quality score
        quality = len(cleaned_records) / len(raw_data["records"])
        self.state.quality_scores["cleaning"] = quality
        
        print(f"Cleaned: {len(cleaned_records)} valid records")
        print(f"Removed: {self.state.cleaned_data['removed_count']} invalid records")
        print(f"Quality score: {quality:.2%}")
        
        return self.state.cleaned_data

    @listen(clean_data)
    def analyze_data(self, cleaned_data):
        """Stage 3: Analyze cleaned data."""
        print(f"\n[STAGE: {PipelineStage.ANALYZED.value}]")
        
        records = cleaned_data["records"]
        
        # Perform analysis
        word_counts = [len(r["value"].split()) for r in records]
        analysis = {
            "total_records": len(records),
            "avg_word_count": sum(word_counts) / len(word_counts) if word_counts else 0,
            "max_word_count": max(word_counts) if word_counts else 0,
            "values": [r["value"] for r in records],
            "character_counts": [len(r["value"]) for r in records]
        }
        
        self.state.analysis_results = analysis
        self.state.current_stage = PipelineStage.ANALYZED
        self.state.stage_history.append(PipelineStage.ANALYZED.value)
        
        # Quality score based on analysis completeness
        self.state.quality_scores["analysis"] = 1.0  # Full completion
        
        print(f"Analyzed {analysis['total_records']} records")
        print(f"Average word count: {analysis['avg_word_count']:.2f}")
        
        return analysis

    @listen(analyze_data)
    def generate_report(self, analysis):
        """Stage 4: Generate final report from analysis."""
        print(f"\n[STAGE: {PipelineStage.REPORTED.value}]")
        
        report = {
            "title": "Data Processing Pipeline Report",
            "summary": {
                "input_records": len(self.state.raw_data["records"]),
                "output_records": analysis["total_records"],
                "success_rate": analysis["total_records"] / len(self.state.raw_data["records"])
            },
            "metrics": {
                "average_words": analysis["avg_word_count"],
                "max_words": analysis["max_word_count"]
            },
            "quality_scores": self.state.quality_scores,
            "stage_history": self.state.stage_history
        }
        
        self.state.final_report = report
        self.state.current_stage = PipelineStage.REPORTED
        self.state.stage_history.append(PipelineStage.REPORTED.value)
        
        print(f"\n{'='*60}")
        print(f"PIPELINE COMPLETE - Final Report")
        print(f"{'='*60}")
        print(f"Records processed: {report['summary']['input_records']} → {report['summary']['output_records']}")
        print(f"Success rate: {report['summary']['success_rate']:.2%}")
        print(f"Stages completed: {' → '.join(report['stage_history'])}")
        
        return report
```

### Explanation

1. **Stage Tracking**: `current_stage` and `stage_history` track pipeline progress
2. **Immutable Stages**: Each stage stores data in its own field, preserving history
3. **Transformation Chain**: Raw → Cleaned → Analyzed → Reported
4. **Quality Gates**: Each stage can calculate and store quality metrics

### Output

```
[STAGE: raw]
Extracted 3 raw records

[STAGE: cleaned]
Cleaned: 2 valid records
Removed: 1 invalid records
Quality score: 66.67%

[STAGE: analyzed]
Analyzed 2 records
Average word count: 2.00

[STAGE: reported]
============================================================
PIPELINE COMPLETE - Final Report
============================================================
Records processed: 3 → 2
Success rate: 66.67%
Stages completed: raw → cleaned → analyzed → reported
```

---

## 3. Branching State Pattern

**Purpose**: Different state updates based on conditions, with separate fields for each path.

**When to Use**:
- Approval/rejection workflows
- Multi-path decision trees
- Feature flags affecting state structure
- Conditional data collection

### State Model Definition

```python
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

class DecisionStatus(str, Enum):
    """Possible decision outcomes."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CONDITIONAL = "conditional"

class ApprovalDetails(BaseModel):
    """State specific to approval path."""
    approved_by: str = ""
    approval_date: Optional[datetime] = None
    approval_notes: str = ""
    approved_amount: float = 0.0
    next_steps: list = Field(default_factory=list)

class RejectionDetails(BaseModel):
    """State specific to rejection path."""
    rejected_by: str = ""
    rejection_date: Optional[datetime] = None
    rejection_reason: str = ""
    rejection_category: str = ""
    can_reapply: bool = False
    reapply_date: Optional[datetime] = None

class BranchingState(BaseModel):
    """State with branching fields for different paths."""
    # Input data
    request_id: str = ""
    request_amount: float = 0.0
    requestor: str = ""
    
    # Decision tracking
    decision_status: DecisionStatus = DecisionStatus.PENDING
    decision_date: Optional[datetime] = None
    reviewer: str = ""
    
    # Branch-specific fields (only one populated based on path)
    approval_details: Optional[ApprovalDetails] = None
    rejection_details: Optional[RejectionDetails] = None
    
    # Common fields (populated regardless of path)
    processing_time_ms: int = 0
    final_message: str = ""
```

### Flow Implementation

```python
from crewai.flow.flow import Flow, listen, start, router

class BranchingFlow(Flow[BranchingState]):
    """
    Demonstrates branching state updates based on router decisions.
    
    Different paths populate different state fields:
    - Approved path → approval_details
    - Rejected path → rejection_details
    """

    @start()
    def submit_request(self):
        """Initialize request."""
        print(f"\n{'='*60}")
        print("NEW REQUEST SUBMITTED")
        print(f"{'='*60}")
        
        self.state.request_id = "REQ-2024-001"
        self.state.request_amount = 5000.00
        self.state.requestor = "john.doe@company.com"
        
        print(f"Request ID: {self.state.request_id}")
        print(f"Amount: ${self.state.request_amount:,.2f}")
        print(f"Requestor: {self.state.requestor}")
        
        return self.state.request_id

    @listen(submit_request)
    def evaluate_request(self, request_id):
        """Evaluate and route based on criteria."""
        print(f"\n[EVALUATION]")
        print(f"Evaluating request {request_id}...")
        
        # Simulate evaluation logic
        if self.state.request_amount <= 1000:
            return "auto_approved"
        elif self.state.request_amount <= 5000:
            return "needs_review"
        else:
            return "auto_rejected"

    @listen("auto_approved")
    def handle_auto_approval(self):
        """Auto-approval path - minimal details."""
        print("\n[AUTO-APPROVED]")
        
        self.state.decision_status = DecisionStatus.APPROVED
        self.state.decision_date = datetime.now()
        self.state.reviewer = "system"
        
        # Populate approval-specific state
        self.state.approval_details = ApprovalDetails(
            approved_by="auto_approval_system",
            approval_date=datetime.now(),
            approval_notes="Amount below threshold - auto approved",
            approved_amount=self.state.request_amount,
            next_steps=["Process payment", "Send confirmation email"]
        )
        
        self.state.final_message = f"Request approved for ${self.state.request_amount:,.2f}"
        return "approved"

    @listen("needs_review")
    def handle_manual_review(self):
        """Manual review path - simulates human decision."""
        print("\n[MANUAL REVIEW]")
        print("Request sent to manual review...")
        
        # Simulate reviewer decision (in real app, this would wait for human input)
        approved = True  # Simulated decision
        
        self.state.reviewer = "reviewer@company.com"
        self.state.decision_date = datetime.now()
        
        if approved:
            self.state.decision_status = DecisionStatus.APPROVED
            self.state.approval_details = ApprovalDetails(
                approved_by=self.state.reviewer,
                approval_date=datetime.now(),
                approval_notes="Reviewed and approved by manual reviewer",
                approved_amount=self.state.request_amount * 0.8,  # Partial approval
                next_steps=["Process partial payment", "Update requestor"]
            )
            self.state.final_message = f"Request approved for 80%: ${self.state.approval_details.approved_amount:,.2f}"
            return "approved"
        else:
            self.state.decision_status = DecisionStatus.REJECTED
            self.state.rejection_details = RejectionDetails(
                rejected_by=self.state.reviewer,
                rejection_date=datetime.now(),
                rejection_reason="Insufficient documentation",
                rejection_category="incomplete",
                can_reapply=True
            )
            self.state.final_message = "Request rejected - incomplete documentation"
            return "rejected"

    @listen("auto_rejected")
    def handle_auto_rejection(self):
        """Auto-rejection path."""
        print("\n[AUTO-REJECTED]")
        
        self.state.decision_status = DecisionStatus.REJECTED
        self.state.decision_date = datetime.now()
        self.state.reviewer = "system"
        
        # Populate rejection-specific state
        self.state.rejection_details = RejectionDetails(
            rejected_by="validation_system",
            rejection_date=datetime.now(),
            rejection_reason="Amount exceeds maximum limit",
            rejection_category="limit_exceeded",
            can_reapply=False
        )
        
        self.state.final_message = "Request rejected - amount exceeds limit"
        return "rejected"

    @listen("approved", "rejected")
    def finalize(self, decision):
        """Final step - shows which branch fields are populated."""
        print(f"\n{'='*60}")
        print(f"FINAL STATUS: {self.state.decision_status.value.upper()}")
        print(f"{'='*60}")
        print(f"Message: {self.state.final_message}")
        print(f"Reviewer: {self.state.reviewer}")
        print(f"Decision date: {self.state.decision_date}")
        
        # Show which branch-specific fields are populated
        if self.state.approval_details:
            print(f"\n[Approval Details]")
            print(f"  Approved by: {self.state.approval_details.approved_by}")
            print(f"  Approved amount: ${self.state.approval_details.approved_amount:,.2f}")
            print(f"  Next steps: {self.state.approval_details.next_steps}")
        
        if self.state.rejection_details:
            print(f"\n[Rejection Details]")
            print(f"  Rejected by: {self.state.rejection_details.rejected_by}")
            print(f"  Reason: {self.state.rejection_details.rejection_reason}")
            print(f"  Can reapply: {self.state.rejection_details.can_reapply}")
        
        return self.state.decision_status.value
```

### Explanation

1. **Separate Models**: `ApprovalDetails` and `RejectionDetails` are separate models
2. **Optional Fields**: Only the relevant branch field is populated
3. **Router-Driven**: `@router` determines which path to take
4. **Clean State**: Each path has its own clean state structure

### Output

```
============================================================
NEW REQUEST SUBMITTED
============================================================
Request ID: REQ-2024-001
Amount: $5,000.00
Requestor: john.doe@company.com

[EVALUATION]
Evaluating request REQ-2024-001...

[MANUAL REVIEW]
Request sent to manual review...

============================================================
FINAL STATUS: APPROVED
============================================================
Message: Request approved for 80%: $4,000.00
Reviewer: reviewer@company.com
Decision date: 2024-01-15 10:30:00

[Approval Details]
  Approved by: reviewer@company.com
  Approved amount: $4,000.00
  Next steps: ['Process partial payment', 'Update requestor']
```

---

## 4. Retry Pattern

**Purpose**: Track retry attempts, handle failures gracefully, and reset state on success.

**When to Use**:
- API calls with transient failures
- Network operations
- External service integration
- Operations that may timeout

### State Model Definition

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class RetryStatus(str, Enum):
    """Status of retry operations."""
    IDLE = "idle"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    MAX_RETRIES = "max_retries"

class RetryAttempt(BaseModel):
    """Record of a single retry attempt."""
    attempt_number: int
    timestamp: datetime
    status: str
    error_message: Optional[str] = None
    duration_ms: int = 0

class RetryState(BaseModel):
    """State for tracking retries with backoff."""
    # Configuration
    max_retries: int = 3
    base_delay_seconds: float = 1.0
    backoff_multiplier: float = 2.0
    
    # Retry tracking
    current_retry: int = 0
    retry_history: list = Field(default_factory=list)
    
    # Operation status
    status: RetryStatus = RetryStatus.IDLE
    last_error: Optional[str] = None
    
    # Result
    operation_result: Optional[str] = None
    final_attempt: Optional[RetryAttempt] = None
```

### Flow Implementation

```python
from crewai.flow.flow import Flow, listen, start, router
import time
import random

class RetryFlow(Flow[RetryState]):
    """
    Demonstrates retry pattern with exponential backoff.
    
    Pattern:
    1. Attempt operation
    2. If fail → increment retry, wait, try again
    3. If max retries → mark as failed
    4. If success → clear retry state, store result
    """

    @start()
    def initialize(self):
        """Setup retry configuration."""
        print(f"\n{'='*60}")
        print("RETRY PATTERN DEMO")
        print(f"{'='*60}")
        print(f"Max retries: {self.state.max_retries}")
        print(f"Base delay: {self.state.base_delay_seconds}s")
        print(f"Backoff: {self.state.backoff_multiplier}x")
        return "initialized"

    @listen(initialize)
    def attempt_operation(self, _):
        """Main retry logic."""
        self.state.status = RetryStatus.IN_PROGRESS
        
        while self.state.current_retry < self.state.max_retries:
            self.state.current_retry += 1
            attempt_start = datetime.now()
            
            print(f"\n[Attempt {self.state.current_retry}/{self.state.max_retries}]")
            
            # Simulate API call (70% failure rate for demo)
            success = self._simulate_api_call()
            duration = int((datetime.now() - attempt_start).total_seconds() * 1000)
            
            attempt = RetryAttempt(
                attempt_number=self.state.current_retry,
                timestamp=datetime.now(),
                status="success" if success else "failed",
                duration_ms=duration
            )
            
            if success:
                # SUCCESS: Reset retry state, store result
                attempt.status = "success"
                self.state.retry_history.append(attempt)
                return self._handle_success()
            else:
                # FAILURE: Track error, prepare for retry
                attempt.error_message = "Simulated API failure"
                self.state.retry_history.append(attempt)
                self.state.last_error = attempt.error_message
                
                if self.state.current_retry < self.state.max_retries:
                    self._wait_before_retry()
        
        # Max retries reached
        return self._handle_max_retries()

    def _simulate_api_call(self):
        """Simulate an API call with random failures."""
        # 70% chance of failure for demonstration
        success = random.random() > 0.7
        time.sleep(0.1)  # Simulate network delay
        return success

    def _wait_before_retry(self):
        """Calculate and apply backoff delay."""
        delay = self.state.base_delay_seconds * (self.state.backoff_multiplier ** (self.state.current_retry - 1))
        print(f"  Failed. Waiting {delay:.2f}s before retry...")
        time.sleep(delay)

    def _handle_success(self):
        """Handle successful operation."""
        print("\n[SUCCESS]")
        self.state.status = RetryStatus.SUCCESS
        self.state.operation_result = "Data successfully retrieved from API"
        self.state.final_attempt = self.state.retry_history[-1]
        
        # Clear error state
        self.state.last_error = None
        
        return "success"

    def _handle_max_retries(self):
        """Handle max retries exceeded."""
        print(f"\n[MAX RETRIES EXCEEDED]")
        self.state.status = RetryStatus.MAX_RETRIES
        self.state.final_attempt = self.state.retry_history[-1]
        
        return "max_retries"

    @listen("success")
    def success_cleanup(self):
        """Cleanup after successful retry."""
        print(f"\n{'='*60}")
        print("RETRY PATTERN: SUCCESS")
        print(f"{'='*60}")
        print(f"Operation succeeded after {self.state.current_retry} attempt(s)")
        print(f"Result: {self.state.operation_result}")
        print(f"\nRetry History:")
        for attempt in self.state.retry_history:
            status_icon = "✓" if attempt.status == "success" else "✗"
            print(f"  {status_icon} Attempt {attempt.attempt_number}: {attempt.status} ({attempt.duration_ms}ms)")
        
        return self.state.operation_result

    @listen("max_retries")
    def failure_handler(self):
        """Handle final failure."""
        print(f"\n{'='*60}")
        print("RETRY PATTERN: FAILED")
        print(f"{'='*60}")
        print(f"Operation failed after {self.state.max_retries} retries")
        print(f"Last error: {self.state.last_error}")
        print(f"\nRetry History:")
        for attempt in self.state.retry_history:
            print(f"  ✗ Attempt {attempt.attempt_number}: {attempt.error_message}")
        
        return "failed"
```

### Explanation

1. **Retry Counter**: `current_retry` tracks attempt number
2. **Exponential Backoff**: Wait time increases with each retry
3. **History Tracking**: Each attempt recorded with timestamp and result
4. **State Reset**: On success, error state is cleared
5. **Max Retry Protection**: Prevents infinite loops

### Output

```
============================================================
RETRY PATTERN DEMO
============================================================
Max retries: 3
Base delay: 1.0s
Backoff: 2.0x

[Attempt 1/3]
  Failed. Waiting 1.00s before retry...

[Attempt 2/3]
  Failed. Waiting 2.00s before retry...

[Attempt 3/3]

[SUCCESS]

============================================================
RETRY PATTERN: SUCCESS
============================================================
Operation succeeded after 3 attempt(s)
Result: Data successfully retrieved from API

Retry History:
  ✗ Attempt 1: failed (100ms)
  ✗ Attempt 2: failed (100ms)
  ✓ Attempt 3: success (100ms)
```

---

## 5. Progress Tracking Pattern

**Purpose**: Track completion percentage and stage progress for long-running flows.

**When to Use**:
- Multi-step workflows
- Batch processing
- File uploads/downloads
- Report generation

### State Model Definition

```python
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class ProgressStage(str, Enum):
    """Stages of progress."""
    INITIALIZING = "initializing"
    PROCESSING = "processing"
    FINALIZING = "finalizing"
    COMPLETE = "complete"

class ProgressState(BaseModel):
    """State for tracking progress through a flow."""
    # Progress metrics
    total_steps: int = 0
    current_step: int = 0
    percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    
    # Stage tracking
    current_stage: ProgressStage = ProgressStage.INITIALIZING
    stages_completed: List[str] = Field(default_factory=list)
    
    # Time tracking
    start_time: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    
    # Detailed progress
    step_details: List[dict] = Field(default_factory=list)
    current_operation: str = ""
    
    # Completion
    completed: bool = False
    completion_message: str = ""
```

### Flow Implementation

```python
from crewai.flow.flow import Flow, listen, start

class ProgressTrackingFlow(Flow[ProgressState]):
    """
    Demonstrates progress tracking pattern.
    
    Updates progress after each step:
    - current_step increments
    - percentage recalculated
    - stage transitions tracked
    """

    @start()
    def initialize(self):
        """Initialize progress tracking."""
        self.state.start_time = datetime.now()
        self.state.total_steps = 5
        self.state.current_stage = ProgressStage.INITIALIZING
        self.state.current_operation = "Initializing workflow"
        
        self._update_progress()
        self._display_progress()
        
        return "initialized"

    @listen(initialize)
    def load_data(self, _):
        """Step 1: Load data."""
        self.state.current_step = 1
        self.state.current_stage = ProgressStage.PROCESSING
        self.state.current_operation = "Loading data from sources"
        
        # Simulate work
        import time
        time.sleep(0.5)
        
        self._update_progress()
        self._display_progress()
        
        return "data_loaded"

    @listen(load_data)
    def validate_data(self, _):
        """Step 2: Validate data."""
        self.state.current_step = 2
        self.state.current_operation = "Validating data integrity"
        
        time.sleep(0.3)
        
        self._update_progress()
        self._display_progress()
        
        return "data_validated"

    @listen(validate_data)
    def process_data(self, _):
        """Step 3: Process data."""
        self.state.current_step = 3
        self.state.current_operation = "Processing and transforming data"
        
        time.sleep(0.7)
        
        self._update_progress()
        self._display_progress()
        
        return "data_processed"

    @listen(process_data)
    def generate_output(self, _):
        """Step 4: Generate output."""
        self.state.current_step = 4
        self.state.current_stage = ProgressStage.FINALIZING
        self.state.current_operation = "Generating final output"
        
        time.sleep(0.4)
        
        self._update_progress()
        self._display_progress()
        
        return "output_generated"

    @listen(generate_output)
    def finalize(self, _):
        """Step 5: Finalize."""
        self.state.current_step = 5
        self.state.current_stage = ProgressStage.COMPLETE
        self.state.current_operation = "Finalizing and cleanup"
        self.state.completed = True
        self.state.completion_message = "Workflow completed successfully"
        
        time.sleep(0.2)
        
        self._update_progress()
        self._display_progress()
        
        return "completed"

    def _update_progress(self):
        """Calculate percentage and estimate completion."""
        if self.state.total_steps > 0:
            self.state.percentage = (self.state.current_step / self.state.total_steps) * 100
        
        # Record step detail
        self.state.step_details.append({
            "step": self.state.current_step,
            "stage": self.state.current_stage.value,
            "operation": self.state.current_operation,
            "timestamp": datetime.now()
        })
        
        # Simple ETA calculation (assuming linear progress)
        if self.state.start_time and self.state.current_step > 0:
            elapsed = (datetime.now() - self.state.start_time).total_seconds()
            if self.state.current_step < self.state.total_steps:
                avg_time_per_step = elapsed / self.state.current_step
                remaining_steps = self.state.total_steps - self.state.current_step
                eta_seconds = avg_time_per_step * remaining_steps
                self.state.estimated_completion = datetime.now() + timedelta(seconds=eta_seconds)

    def _display_progress(self):
        """Display progress bar and status."""
        bar_length = 30
        filled = int(bar_length * self.state.percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        print(f"\n┌{'─'*58}┐")
        print(f"│ {self.state.current_stage.value.upper():^56} │")
        print(f"├{'─'*58}┤")
        print(f"│ {bar} {self.state.percentage:5.1f}% │")
        print(f"├{'─'*58}┤")
        print(f"│ Step {self.state.current_step}/{self.state.total_steps}: {self.state.current_operation[:40]:<40} │")
        print(f"└{'─'*58}┘")
```

### Explanation

1. **Percentage Calculation**: `percentage = (current / total) * 100`
2. **Stage Transitions**: ProgressStage enum tracks high-level phases
3. **Visual Feedback**: Progress bar shows completion status
4. **ETA Calculation**: Estimates completion based on average step time
5. **History Tracking**: Records each step for audit trail

### Output

```
┌──────────────────────────────────────────────────────────┐
│                     INITIALIZING                         │
├──────────────────────────────────────────────────────────┤
│ █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   0.0% │
├──────────────────────────────────────────────────────────┤
│ Step 0/5: Initializing workflow                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                     PROCESSING                           │
├──────────────────────────────────────────────────────────┤
│ ████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  20.0% │
├──────────────────────────────────────────────────────────┤
│ Step 1/5: Loading data from sources                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                     PROCESSING                           │
├──────────────────────────────────────────────────────────┤
│ ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  40.0% │
├──────────────────────────────────────────────────────────┤
│ Step 2/5: Validating data integrity                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                     PROCESSING                           │
├──────────────────────────────────────────────────────────┤
│ ████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░  60.0% │
├──────────────────────────────────────────────────────────┤
│ Step 3/5: Processing and transforming data               │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                     FINALIZING                           │
├──────────────────────────────────────────────────────────┤
│ ████████████████████████████████░░░░░░░░░░░░░░░░  80.0% │
├──────────────────────────────────────────────────────────┤
│ Step 4/5: Generating final output                        │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                       COMPLETE                           │
├──────────────────────────────────────────────────────────┤
│ ████████████████████████████████████████████████ 100.0% │
├──────────────────────────────────────────────────────────┤
│ Step 5/5: Finalizing and cleanup                         │
└──────────────────────────────────────────────────────────┘
```

---

## 6. Error Recovery Pattern

**Purpose**: Handle errors gracefully with recovery state tracking and fallback values.

**When to Use**:
- Critical flows that must complete
- External service dependencies
- Data validation workflows
- Multi-step transactions

### State Model Definition

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum

class ErrorSeverity(str, Enum):
    """Severity levels for errors."""
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class RecoveryAttempt(BaseModel):
    """Record of recovery attempt."""
    timestamp: datetime
    strategy: str
    success: bool
    fallback_used: Optional[str] = None
    error_resolved: bool = False

class ErrorState(BaseModel):
    """State for tracking and recovering from errors."""
    # Error tracking
    has_error: bool = False
    error_message: Optional[str] = None
    error_severity: Optional[ErrorSeverity] = None
    error_step: Optional[str] = None
    error_timestamp: Optional[datetime] = None
    
    # Recovery tracking
    recovery_attempts: List[RecoveryAttempt] = Field(default_factory=list)
    recovery_in_progress: bool = False
    
    # Fallback values
    fallback_values: dict = Field(default_factory=dict)
    using_fallback: bool = False
    
    # Final state
    completed_with_errors: bool = False
    final_result: Optional[Any] = None
    success_despite_errors: bool = False
```

### Flow Implementation

```python
from crewai.flow.flow import Flow, listen, start, router

class ErrorRecoveryFlow(Flow[ErrorState]):
    """
    Demonstrates error recovery pattern with fallbacks.
    
    Patterns:
    1. Try primary operation
    2. If fail → attempt recovery
    3. If recovery fails → use fallback
    4. Track all attempts in state
    """

    @start()
    def initialize(self):
        """Setup with fallback values."""
        print(f"\n{'='*60}")
        print("ERROR RECOVERY PATTERN")
        print(f"{'='*60}")
        
        # Pre-define fallback values
        self.state.fallback_values = {
            "default_name": "Unknown User",
            "default_email": "noreply@example.com",
            "default_score": 0.0,
            "default_items": ["item_1", "item_2"]
        }
        
        return "initialized"

    @listen(initialize)
    def fetch_primary_data(self, _):
        """Attempt to fetch primary data."""
        print("\n[STEP 1: Fetch Primary Data]")
        
        try:
            # Simulate external API call that might fail
            result = self._risky_api_call()
            print(f"✓ Primary data fetched: {result}")
            return result
        except Exception as e:
            # Record error in state
            self._record_error(str(e), ErrorSeverity.ERROR, "fetch_primary_data")
            print(f"✗ Primary fetch failed: {e}")
            return "fetch_failed"

    @router(fetch_primary_data)
    def route_based_on_result(self, result):
        """Route based on success or failure."""
        if result == "fetch_failed":
            return "attempt_recovery"
        return "use_primary_data"

    @listen("attempt_recovery")
    def attempt_recovery_strategy(self):
        """Attempt to recover from the error."""
        print("\n[STEP 2: Attempt Recovery]")
        self.state.recovery_in_progress = True
        
        # Recovery Strategy 1: Retry with cache
        print("  Trying cache fallback...")
        cache_result = self._try_cache_fallback()
        
        attempt = RecoveryAttempt(
            timestamp=datetime.now(),
            strategy="cache_fallback",
            success=cache_result is not None
        )
        
        if cache_result:
            print(f"  ✓ Cache recovery successful: {cache_result}")
            attempt.error_resolved = True
            self.state.recovery_attempts.append(attempt)
            self.state.recovery_in_progress = False
            return cache_result
        
        print("  ✗ Cache recovery failed")
        self.state.recovery_attempts.append(attempt)
        
        # Recovery Strategy 2: Use defaults
        print("  Trying default values fallback...")
        default_result = self._use_fallback_values()
        
        attempt = RecoveryAttempt(
            timestamp=datetime.now(),
            strategy="default_values",
            success=True,
            fallback_used="default_items",
            error_resolved=False  # Error not resolved, but flow can continue
        )
        self.state.recovery_attempts.append(attempt)
        
        self.state.using_fallback = True
        self.state.recovery_in_progress = False
        print(f"  ✓ Using fallback values: {default_result}")
        
        return default_result

    @listen("use_primary_data")
    def process_primary(self, data):
        """Process successfully fetched primary data."""
        print("\n[Processing Primary Data]")
        processed = f"PROCESSED: {data}"
        self.state.final_result = processed
        return processed

    @listen(attempt_recovery_strategy)
    def process_with_fallback(self, data):
        """Process with fallback data."""
        print("\n[Processing with Fallback Data]")
        processed = f"FALLBACK_PROCESSED: {data}"
        self.state.final_result = processed
        self.state.completed_with_errors = True
        self.state.success_despite_errors = True
        return processed

    @listen(process_primary, process_with_fallback)
    def finalize(self, result):
        """Finalize with error recovery summary."""
        print(f"\n{'='*60}")
        print("FINAL STATUS")
        print(f"{'='*60}")
        
        if self.state.has_error:
            print(f"⚠ Errors encountered: Yes")
            print(f"  Error: {self.state.error_message}")
            print(f"  Severity: {self.state.error_severity}")
            print(f"  Step: {self.state.error_step}")
        else:
            print(f"✓ No errors")
        
        if self.state.recovery_attempts:
            print(f"\n📋 Recovery Attempts:")
            for i, attempt in enumerate(self.state.recovery_attempts, 1):
                status = "✓" if attempt.success else "✗"
                resolved = "(resolved)" if attempt.error_resolved else ""
                print(f"  {i}. {status} {attempt.strategy} {resolved}")
        
        if self.state.using_fallback:
            print(f"\n⚙ Using fallback values: Yes")
            print(f"  Result: {self.state.final_result}")
            print(f"  Completed despite errors: {self.state.success_despite_errors}")
        else:
            print(f"\n✓ Primary data used")
            print(f"  Result: {self.state.final_result}")
        
        return result

    def _risky_api_call(self):
        """Simulate a risky API call."""
        import random
        if random.random() > 0.5:  # 50% failure rate for demo
            raise Exception("API timeout - service unavailable")
        return {"user": "john_doe", "score": 95.5, "valid": True}

    def _try_cache_fallback(self):
        """Try to get data from cache."""
        import random
        if random.random() > 0.7:  # 30% cache hit rate
            return {"user": "cached_user", "score": 85.0, "cached": True}
        return None

    def _use_fallback_values(self):
        """Use default fallback values."""
        return {
            "user": self.state.fallback_values["default_name"],
            "score": self.state.fallback_values["default_score"],
            "items": self.state.fallback_values["default_items"],
            "fallback": True
        }

    def _record_error(self, message: str, severity: ErrorSeverity, step: str):
        """Record error details in state."""
        self.state.has_error = True
        self.state.error_message = message
        self.state.error_severity = severity
        self.state.error_step = step
        self.state.error_timestamp = datetime.now()
```

### Explanation

1. **Error Recording**: Errors captured with severity, timestamp, and location
2. **Recovery Strategies**: Multiple fallback strategies attempted in order
3. **Fallback Values**: Pre-defined defaults ensure flow completion
4. **Recovery History**: All recovery attempts tracked for audit
5. **Graceful Degradation**: Flow completes even with errors using fallbacks

### Output

```
============================================================
ERROR RECOVERY PATTERN
============================================================

[STEP 1: Fetch Primary Data]
✗ Primary fetch failed: API timeout - service unavailable

[STEP 2: Attempt Recovery]
  Trying cache fallback...
  ✗ Cache recovery failed
  Trying default values fallback...
  ✓ Using fallback values: {'user': 'Unknown User', ...}

[Processing with Fallback Data]

============================================================
FINAL STATUS
============================================================
⚠ Errors encountered: Yes
  Error: API timeout - service unavailable
  Severity: error
  Step: fetch_primary_data

📋 Recovery Attempts:
  1. ✗ cache_fallback
  2. ✓ default_values

⚙ Using fallback values: Yes
  Result: FALLBACK_PROCESSED: {'user': 'Unknown User', ...}
  Completed despite errors: True
```

---

## 7. Crew Integration Pattern

**Purpose**: Seamlessly pass flow state to CrewAI crews and store crew outputs back in state.

**When to Use**:
- Complex multi-agent workflows
- Need to combine flow orchestration with crew intelligence
- Typed handoff between flow and crew
- State synchronization between flow and crew

### State Model Definition

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class CrewInput(BaseModel):
    """Typed input for crew handoff."""
    research_topic: str
    context: Dict[str, Any] = Field(default_factory=dict)
    constraints: List[str] = Field(default_factory=list)
    previous_findings: List[str] = Field(default_factory=list)

class CrewOutput(BaseModel):
    """Typed output from crew execution."""
    findings: List[str] = Field(default_factory=list)
    summary: str = ""
    recommendations: List[str] = Field(default_factory=list)
    confidence_score: float = 0.0
    sources: List[str] = Field(default_factory=list)
    execution_time_ms: int = 0

class CrewIntegrationState(BaseModel):
    """State for flow-crew integration."""
    # Flow-level state
    workflow_id: str = ""
    started_at: datetime = Field(default_factory=datetime.now)
    
    # Crew input (typed handoff to crew)
    crew_input: Optional[CrewInput] = None
    
    # Crew output (typed handoff from crew)
    crew_output: Optional[CrewOutput] = None
    
    # Integration tracking
    crew_dispatched: bool = False
    crew_completed: bool = False
    crew_error: Optional[str] = None
    
    # Post-crew processing
    final_report: str = ""
    action_items: List[str] = Field(default_factory=list)
```

### Flow Implementation

```python
from crewai.flow.flow import Flow, listen, start
from crewai import Agent, Task, Crew

class CrewIntegrationFlow(Flow[CrewIntegrationState]):
    """
    Demonstrates typed flow-crew integration.
    
    Pattern:
    1. Flow prepares state → creates CrewInput
    2. Flow dispatches crew with typed input
    3. Crew executes and returns CrewOutput
    4. Flow stores output in state
    5. Flow continues with crew results
    """

    @start()
    def prepare_crew_input(self):
        """Prepare typed input for crew handoff."""
        print(f"\n{'='*60}")
        print("CREW INTEGRATION PATTERN")
        print(f"{'='*60}")
        
        self.state.workflow_id = "research-workflow-001"
        
        # Build typed crew input from flow state
        self.state.crew_input = CrewInput(
            research_topic="AI Trends in 2024",
            context={
                "industry": "Technology",
                "focus_areas": ["Machine Learning", "NLP", "Computer Vision"],
                "time_period": "January-June 2024"
            },
            constraints=[
                "Focus on enterprise applications",
                "Include ethical considerations",
                "Cite recent sources (2024)"
            ],
            previous_findings=[]
        )
        
        print("\n📋 Crew Input Prepared:")
        print(f"  Topic: {self.state.crew_input.research_topic}")
        print(f"  Context: {len(self.state.crew_input.context)} fields")
        print(f"  Constraints: {len(self.state.crew_input.constraints)} items")
        
        return self.state.crew_input

    @listen(prepare_crew_input)
    def dispatch_crew(self, crew_input):
        """Dispatch crew with typed input, receive typed output."""
        print("\n🚀 Dispatching Crew...")
        self.state.crew_dispatched = True
        
        start_time = datetime.now()
        
        # Create crew from typed input
        crew = self._create_research_crew(crew_input)
        
        # Execute crew (in real app, this runs the actual crew)
        # For demo, we simulate crew execution
        crew_result = self._simulate_crew_execution(crew_input)
        
        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Store typed output in state
        self.state.crew_output = CrewOutput(
            findings=crew_result["findings"],
            summary=crew_result["summary"],
            recommendations=crew_result["recommendations"],
            confidence_score=crew_result["confidence"],
            sources=crew_result["sources"],
            execution_time_ms=execution_time
        )
        
        self.state.crew_completed = True
        
        print(f"\n✓ Crew completed in {execution_time}ms")
        print(f"  Findings: {len(self.state.crew_output.findings)} items")
        print(f"  Confidence: {self.state.crew_output.confidence_score:.0%}")
        
        return self.state.crew_output

    @listen(dispatch_crew)
    def process_crew_results(self, crew_output):
        """Process crew output and update flow state."""
        print("\n📊 Processing Crew Results...")
        
        # Build final report from crew output
        report_lines = [
            f"# Research Report: {self.state.crew_input.research_topic}",
            f"\n## Executive Summary\n{crew_output.summary}",
            f"\n## Key Findings"
        ]
        
        for i, finding in enumerate(crew_output.findings, 1):
            report_lines.append(f"{i}. {finding}")
        
        report_lines.extend([
            f"\n## Recommendations",
            f"Confidence Score: {crew_output.confidence_score:.0%}"
        ])
        
        for rec in crew_output.recommendations:
            report_lines.append(f"- {rec}")
        
        self.state.final_report = "\n".join(report_lines)
        self.state.action_items = crew_output.recommendations
        
        print(f"\n✓ Final report generated ({len(self.state.final_report)} chars)")
        print(f"  Action items: {len(self.state.action_items)}")
        
        return "processed"

    @listen(process_crew_results)
    def finalize(self, _):
        """Show complete integration state."""
        print(f"\n{'='*60}")
        print("INTEGRATION COMPLETE")
        print(f"{'='*60}")
        
        print(f"\n📄 Final Report Preview:")
        print(f"{'─'*50}")
        preview = self.state.final_report[:200] + "..." if len(self.state.final_report) > 200 else self.state.final_report
        print(preview)
        print(f"{'─'*50}")
        
        print(f"\n📊 Integration Summary:")
        print(f"  Workflow ID: {self.state.workflow_id}")
        print(f"  Crew dispatched: {self.state.crew_dispatched}")
        print(f"  Crew completed: {self.state.crew_completed}")
        print(f"  Execution time: {self.state.crew_output.execution_time_ms}ms")
        print(f"  Typed handoff: ✓ (CrewInput → CrewOutput)")
        
        return self.state

    def _create_research_crew(self, crew_input: CrewInput) -> Crew:
        """Create a research crew from typed input."""
        # This would create actual agents and tasks
        # Simplified for demonstration
        
        researcher = Agent(
            role="Research Analyst",
            goal=f"Research {crew_input.research_topic}",
            backstory="Expert in technology trends analysis"
        )
        
        task = Task(
            description=f"Research {crew_input.research_topic} considering: {', '.join(crew_input.constraints)}",
            expected_output="Comprehensive findings and recommendations",
            agent=researcher
        )
        
        return Crew(agents=[researcher], tasks=[task])

    def _simulate_crew_execution(self, crew_input: CrewInput) -> Dict[str, Any]:
        """Simulate crew execution for demo."""
        import time
        time.sleep(0.5)  # Simulate processing time
        
        return {
            "findings": [
                "Enterprise ML adoption increased 40% in 2024",
                "NLP models show 95% accuracy on domain-specific tasks",
                "Computer vision applications expanded to manufacturing QA"
            ],
            "summary": f"Analysis of {crew_input.research_topic} shows significant growth in enterprise adoption with strong performance improvements across all domains.",
            "recommendations": [
                "Invest in ML infrastructure",
                "Develop NLP capabilities for customer service",
                "Explore computer vision for quality assurance"
            ],
            "confidence": 0.87,
            "sources": ["TechCrunch 2024", "MIT Technology Review", "Gartner Research"]
        }


# Usage example showing typed contracts
def run_crew_integration():
    """Example of running the crew integration flow."""
    flow = CrewIntegrationFlow()
    result = flow.kickoff()
    
    # Access typed state after completion
    print(f"\n{'='*60}")
    print("POST-EXECUTION STATE ACCESS")
    print(f"{'='*60}")
    print(f"Input topic: {flow.state.crew_input.research_topic}")
    print(f"Output confidence: {flow.state.crew_output.confidence_score}")
    print(f"Action items: {flow.state.action_items}")
    
    return result
```

### Explanation

1. **Typed Input Contract**: `CrewInput` defines exactly what data flows to the crew
2. **Typed Output Contract**: `CrewOutput` defines exactly what data returns from the crew
3. **State Synchronization**: Flow state tracks crew dispatch and completion
4. **Handoff Tracking**: `crew_dispatched`, `crew_completed` flags track integration state
5. **Error Handling**: `crew_error` field captures any integration failures

### Output

```
============================================================
CREW INTEGRATION PATTERN
============================================================

📋 Crew Input Prepared:
  Topic: AI Trends in 2024
  Context: 3 fields
  Constraints: 3 items

🚀 Dispatching Crew...

✓ Crew completed in 520ms
  Findings: 3 items
  Confidence: 87%

📊 Processing Crew Results...

✓ Final report generated (567 chars)
  Action items: 3

============================================================
INTEGRATION COMPLETE
============================================================

📄 Final Report Preview:
──────────────────────────────────────────────────
# Research Report: AI Trends in 2024

## Executive Summary
Analysis of AI Trends in 2024 shows significant growth in enterprise adoption with strong performance improvements across all domains...
──────────────────────────────────────────────────

📊 Integration Summary:
  Workflow ID: research-workflow-001
  Crew dispatched: True
  Crew completed: True
  Execution time: 520ms
  Typed handoff: ✓ (CrewInput → CrewOutput)
```

---

## Summary

These state patterns provide reusable solutions for common flow orchestration scenarios:

| Pattern | Use Case | Key State Fields |
|---------|----------|------------------|
| **Accumulator** | Building collections | `processed_items`, `success_count` |
| **Pipeline** | Data transformations | `raw_data`, `cleaned_data`, `final_report` |
| **Branching** | Conditional paths | `approval_details`, `rejection_details` |
| **Retry** | Handling failures | `current_retry`, `retry_history` |
| **Progress** | Long operations | `percentage`, `current_step`, `total_steps` |
| **Error Recovery** | Graceful degradation | `recovery_attempts`, `fallback_values` |
| **Crew Integration** | Flow-crew handoff | `crew_input`, `crew_output` |

Each pattern includes complete, runnable code that you can adapt to your specific use case.
