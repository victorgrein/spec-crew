# State Management Reference

## State Approaches

### Unstructured State (Dict-like)

Use dictionary-style access for flexibility.

```python
from crewai.flow.flow import Flow, start, listen

class UnstructuredFlow(Flow):
    @start()
    def initialize(self):
        # Create state dynamically
        self.state["user_name"] = "Alice"
        self.state["count"] = 0
        self.state["items"] = []
        return "Initialized"

    @listen(initialize)
    def add_data(self):
        # Modify existing keys
        self.state["count"] += 1
        self.state["items"].append(f"item_{self.state['count']}")
        return f"Count: {self.state['count']}"

    @listen(add_data)
    def read_data(self):
        # Access nested data
        user = self.state.get("user_name", "Unknown")
        count = self.state["count"]
        return f"User: {user}, Items: {count}"
```

**Best for:**
- Simple flows
- Dynamic schemas
- Prototyping
- When field names aren't known upfront

### Structured State (Pydantic)

Use Pydantic models for type safety.

```python
from pydantic import BaseModel
from typing import List, Optional
from crewai.flow.flow import Flow, start, listen

class MyFlowState(BaseModel):
    user_name: str = ""
    count: int = 0
    items: List[str] = []
    metadata: Optional[dict] = None

class StructuredFlow(Flow[MyFlowState]):
    @start()
    def initialize(self):
        self.state.user_name = "Bob"
        self.state.metadata = {"created": "2024-01-01"}
        return "Initialized"

    @listen(initialize)
    def add_item(self):
        self.state.count += 1
        self.state.items.append(f"item_{self.state.count}")
        return f"Added item {self.state.count}"

    @listen(add_item)
    def summarize(self):
        # Type-safe access
        return {
            "user": self.state.user_name,
            "total_items": len(self.state.items),
            "items": self.state.items
        }
```

**Best for:**
- Complex flows
- Team collaboration
- IDE autocomplete
- Validation requirements

---

## State Lifecycle

### 1. Initialization

State is created when flow starts:

```python
from crewai.flow.flow import Flow, start

class LifecycleFlow(Flow):
    def __init__(self):
        super().__init__()
        # Pre-initialize values
        self.initial_config = {"timeout": 30}

    @start()
    def initialize_state(self):
        # State available here
        self.state.config = self.initial_config
        self.state.start_time = datetime.now()
        self.state.steps_completed = []
        return "State initialized"
```

### 2. Modification During Execution

```python
class ModificationFlow(Flow):
    @start()
    def step_one(self):
        self.state.phase = "gathering"
        self.state.data = []
        return "Phase: gathering"

    @listen(step_one)
    def step_two(self):
        # Modify existing data
        self.state.phase = "processing"
        self.state.data.append("item_1")
        self.state.data.append("item_2")
        return "Phase: processing"

    @listen(step_two)
    def step_three(self):
        # Transform data
        self.state.phase = "complete"
        self.state.summary = {
            "count": len(self.state.data),
            "items": self.state.data.copy()
        }
        return "Phase: complete"
```

### 3. Transmission Between Methods

```python
class TransmissionFlow(Flow):
    @start()
    def create_data(self):
        data = {
            "id": "123",
            "value": 42,
            "nested": {"key": "value"}
        }
        self.state.original = data
        return data  # Passed to next method

    @listen(create_data)
    def transform_data(self, received_data):
        # received_data contains the returned data
        transformed = {
            "id": received_data["id"],
            "doubled": received_data["value"] * 2,
            "nested_value": received_data["nested"]["key"]
        }
        self.state.transformed = transformed
        return transformed

    @listen(transform_data)
    def finalize(self, final_data):
        # Access both state and received data
        self.state.final = final_data
        return f"Processed: {final_data['id']}"
```

### 4. Persistence (Optional)

```python
from crewai.flow.flow import Flow, start, listen, persist

@persist()
class PersistentStateFlow(Flow):
    @start()
    def checkpoint_1(self):
        self.state.checkpoint = 1
        self.state.data = {"step": "initial"}
        return "Checkpoint 1"

    @listen(checkpoint_1)
    def checkpoint_2(self):
        self.state.checkpoint = 2
        self.state.data["step"] = "middle"
        # State automatically saved here
        return "Checkpoint 2"

    @listen(checkpoint_2)
    def checkpoint_3(self):
        self.state.checkpoint = 3
        self.state.data["step"] = "final"
        # State saved again
        return "Checkpoint 3"
```

### 5. Completion

```python
class CompletionFlow(Flow):
    @start()
    def process(self):
        self.state.status = "running"
        self.state.results = []
        return "Processing"

    @listen(process)
    def finalize(self):
        self.state.status = "complete"
        self.state.results.append("done")
        # State contains all accumulated data
        return self.state

    # After kickoff() returns:
    # flow.state contains final state
```

---

## Automatic State ID

### Unstructured State

```python
from crewai.flow.flow import Flow, start

class UnstructuredIdFlow(Flow):
    @start()
    def show_id(self):
        # Auto-generated UUID
        flow_id = self.state["id"]
        print(f"Flow ID: {flow_id}")
        
        # Use for tracking
        self.state["tracking_id"] = flow_id
        return flow_id
```

### Structured State

```python
from pydantic import BaseModel
from crewai.flow.flow import Flow, start

class StateWithId(BaseModel):
    id: str  # Auto-populated
    name: str = ""
    data: dict = {}

class StructuredIdFlow(Flow[StateWithId]):
    @start()
    def show_id(self):
        # Access auto-generated ID
        print(f"Flow ID: {self.state.id}")
        
        self.state.name = "Example Flow"
        return self.state.id
```

### UUID Format

```python
# Example ID format: "550e8400-e29b-41d4-a716-446655440000"
# Standard UUID v4

class TrackingFlow(Flow):
    @start()
    def log_start(self):
        flow_id = self.state["id"]
        
        # Log to external system
        logger.info(f"Flow {flow_id} started")
        
        # Store for correlation
        self.state["correlation_id"] = flow_id
        
        return flow_id
```

---

## Dynamic State Updates

### Adding Fields Dynamically

```python
from crewai.flow.flow import Flow, start, listen

class DynamicFlow(Flow):
    @start()
    def initial_step(self):
        # Start with minimal state
        self.state.known_field = "value"
        return "Step 1"

    @listen(initial_step)
    def add_fields(self):
        # Add new fields dynamically
        self.state.new_field = "new_value"
        self.state.dynamic_list = []
        self.state.dynamic_dict = {}
        return "Fields added"

    @listen(add_fields)
    def populate_fields(self):
        # Populate dynamically added fields
        self.state.dynamic_list.extend([1, 2, 3])
        self.state.dynamic_dict["key"] = "value"
        self.state.another_new = {"nested": "data"}
        return "Fields populated"
```

### Modifying Nested Data

```python
class NestedDataFlow(Flow):
    @start()
    def setup_structure(self):
        self.state.config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "admin",
                    "password": None
                }
            }
        }
        return "Structure created"

    @listen(setup_structure)
    def modify_nested(self):
        # Modify nested values
        self.state.config["database"]["port"] = 3306
        self.state.config["database"]["credentials"]["password"] = "secret"
        
        # Add nested structure
        self.state.config["cache"] = {
            "enabled": True,
            "ttl": 300
        }
        
        return "Nested data modified"

    @listen(modify_nested)
    def access_nested(self):
        host = self.state.config["database"]["host"]
        port = self.state.config["database"]["port"]
        return f"Database: {host}:{port}"
```

### Type Safety Considerations

```python
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class SafeState(BaseModel):
    # Define expected types
    count: int = 0
    items: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    optional_field: Optional[str] = None

class TypeSafeFlow(Flow[SafeState]):
    @start()
    def valid_operations(self):
        # These are type-safe
        self.state.count += 1
        self.state.items.append("item")
        self.state.metadata["key"] = "value"
        self.state.optional_field = "present"
        return "Valid operations"

    @listen(valid_operations)
    def more_operations(self):
        # Still type-safe
        self.state.items.extend(["a", "b", "c"])
        self.state.metadata.update({"new": "data"})
        
        # This would cause validation error with Pydantic:
        # self.state.count = "string"  # Type error!
        
        return "More operations"
```

---

## Persistence with @persist

### How It Works

```python
from crewai.flow.flow import Flow, start, listen, persist

@persist()
class PersistentFlow(Flow):
    @start()
    def step_one(self):
        self.state.progress = 0.25
        self.state.data = ["a"]
        # State automatically saved here
        return "Step 1"

    @listen(step_one)
    def step_two(self):
        self.state.progress = 0.50
        self.state.data.append("b")
        # State saved again
        return "Step 2"
```

### Class-Level vs Method-Level

**Class-level (all methods):**
```python
@persist()
class FullyPersistentFlow(Flow):
    @start()
    def step_one(self):
        self.state.value = 1
        return "1"  # Saved

    @listen(step_one)
    def step_two(self):
        self.state.value = 2
        return "2"  # Saved

    @listen(step_two)
    def step_three(self):
        self.state.value = 3
        return "3"  # Saved
```

**Method-level (selective):**
```python
class SelectivePersistenceFlow(Flow):
    @start()
    def step_one(self):
        self.state.value = 1
        return "1"  # Not saved

    @persist()
    @listen(step_one)
    def critical_step(self):
        self.state.value = 2
        self.state.important = "data"
        return "2"  # Saved

    @listen(critical_step)
    def step_three(self):
        self.state.value = 3
        return "3"  # Not saved
```

### Resume Behavior

```python
from crewai.flow.flow import Flow, start, listen, persist
from crewai.flow.persistence import SQLitePersistence

@persist(persistence=SQLitePersistence(db_path="./my_flows.db"))
class ResumableFlow(Flow):
    @start()
    def initialize(self):
        if hasattr(self.state, 'resumed'):
            return f"Resumed at step {self.state.last_step}"
        
        self.status = "new"
        self.state.last_step = "initialize"
        return "New flow"

    @listen(initialize)
    def process(self):
        self.state.last_step = "process"
        self.state.processed = True
        return "Processed"

# Resume usage:
# flow = ResumableFlow()
# flow.resume(flow_id="previous-id")
# result = flow.kickoff()
```

### Recovery Patterns

```python
from crewai.flow.flow import Flow, start, listen, persist

@persist()
class RecoverableFlow(Flow):
    @start()
    def initialize(self):
        self.state.attempt = self.state.get("attempt", 0) + 1
        self.state.status = "running"
        return "Initialized"

    @listen(initialize)
    def risky_operation(self):
        try:
            # Simulate work
            if self.state.attempt < 3:
                raise Exception("Temporary failure")
            
            self.state.status = "success"
            self.state.result = "completed"
            return "Success"
        
        except Exception as e:
            self.state.status = "error"
            self.state.error = str(e)
            raise

# Recovery:
# 1. Flow fails, state saved with error
# 2. Fix the issue
# 3. Resume with same flow ID
# 4. Flow continues from last successful step
```

---

## State Best Practices

### 1. Keep State Minimal

```python
# GOOD: Store only necessary data
class MinimalStateFlow(Flow):
    @start()
    def process(self):
        self.state.user_id = "123"
        self.state.decision = "approve"
        # Don't store entire user object if only ID needed
        return "Done"

# BAD: Storing excessive data
class BloatedStateFlow(Flow):
    @start()
    def process(self):
        self.state.user = {
            "id": "123",
            "name": "Alice",
            "email": "alice@example.com",
            "address": {...},  # Not needed
            "preferences": {...}  # Not needed
        }
        return "Done"
```

### 2. Use Structured State for Complex Flows

```python
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    ERROR = "error"

class WorkflowState(BaseModel):
    status: Status = Status.PENDING
    user_id: str = ""
    steps_completed: List[str] = []
    result: Optional[dict] = None
    error_message: Optional[str] = None

class WellStructuredFlow(Flow[WorkflowState]):
    @start()
    def initialize(self):
        self.state.status = Status.RUNNING
        self.state.user_id = "user_123"
        return "Initialized"

    @listen(initialize)
    def process(self):
        self.state.steps_completed.append("initialize")
        # Type-safe status update
        self.state.status = Status.COMPLETE
        self.state.result = {"success": True}
        return "Complete"
```

### 3. Document State Transitions

```python
class DocumentedFlow(Flow):
    """
    State transitions:
    1. initialize: state.input set
    2. validate: state.valid set (True/False)
    3. process (if valid): state.result set
    4. error (if invalid): state.error set
    """
    
    @start()
    def initialize(self):
        """Sets: state.input"""
        self.state.input = self.get_input()
        return "Initialized"

    @listen(initialize)
    def validate(self):
        """Sets: state.valid (bool)"""
        self.state.valid = self.check_validity(self.state.input)
        return self.state.valid

    @listen(validate)
    def process(self, is_valid):
        """Sets: state.result (if valid)"""
        if is_valid:
            self.state.result = self.do_processing()
        return "Processed"
```

### 4. Handle Errors Gracefully

```python
from crewai.flow.flow import Flow, start, listen

class ErrorAwareFlow(Flow):
    @start()
    def initialize(self):
        self.state.error = None
        self.state.result = None
        self.state.status = "starting"
        return "Initialized"

    @listen(initialize)
    def risky_operation(self):
        try:
            self.state.status = "processing"
            result = self.do_risky_work()
            self.state.result = result
            self.state.status = "success"
            return result
        
        except Exception as e:
            self.state.error = {
                "message": str(e),
                "type": type(e).__name__,
                "step": "risky_operation"
            }
            self.state.status = "error"
            # Return error info instead of raising
            return {"error": self.state.error}

    @listen(risky_operation)
    def finalize(self, previous_result):
        if self.state.status == "error":
            # Handle error case
            return f"Failed: {self.state.error['message']}"
        
        # Handle success case
        return f"Success: {self.state.result}"
```

---

## Summary

| Approach | Use When | Example |
|----------|----------|---------|
| Unstructured | Simple, dynamic | `self.state["key"]` |
| Structured | Complex, team work | Pydantic BaseModel |
| Persistence | Long-running, recovery | `@persist()` |
| Minimal | Performance critical | Only store IDs |
| Documented | Team collaboration | Comments, docstrings |
