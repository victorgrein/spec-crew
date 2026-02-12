# Flow Decorators Reference

## @start()

Marks a method as the entry point for a flow execution.

### Unconditional Start

Simplest form - method runs when flow starts.

```python
from crewai.flow.flow import Flow, start

class MyFlow(Flow):
    @start()
    def initialize(self):
        self.state.message = "Flow started"
        return self.state.message
```

### Conditional Start

Start based on another method's completion or a condition.

**Method reference:**
```python
class MyFlow(Flow):
    @start("check_prerequisites")
    def initialize(self):
        # Runs after check_prerequisites completes
        self.state.ready = True

    def check_prerequisites(self):
        return {"prerequisites_met": True}
```

**Callable condition:**
```python
from crewai.flow.flow import Flow, start

class MyFlow(Flow):
    def should_start(self):
        return self.state.get("trigger", False)

    @start(should_start)
    def conditional_start(self):
        self.state.started = True
```

### Return Behavior

The return value is passed to listeners:

```python
class MyFlow(Flow):
    @start()
    def get_user_input(self):
        user_data = {"name": "Alice", "query": "Hello"}
        return user_data  # Passed to @listen handlers

    @listen(get_user_input)
    def process_input(self, user_data):
        # user_data contains {"name": "Alice", "query": "Hello"}
        return f"Processing: {user_data['query']}"
```

---

## @listen()

Waits for other methods to complete before executing.

### Single Source

Listen to one specific method:

```python
from crewai.flow.flow import Flow, start, listen

class MyFlow(Flow):
    @start()
    def step_one(self):
        return "Step 1 complete"

    @listen(step_one)
    def step_two(self, result):
        # result = "Step 1 complete"
        return f"Received: {result}"
```

### Multiple Sources (and_)

Wait for ALL methods to complete (fan-in):

```python
from crewai.flow.flow import Flow, start, listen, and_

class MyFlow(Flow):
    @start()
    def fetch_user_data(self):
        return {"user": "Alice"}

    @start()
    def fetch_order_data(self):
        return {"order": "12345"}

    @listen(and_(fetch_user_data, fetch_order_data))
    def combine_data(self, user_result, order_result):
        # Both methods must complete
        return {
            "user": user_result["user"],
            "order": order_result["order"]
        }
```

### Alternative Sources (or_)

Continue when ANY method completes:

```python
from crewai.flow.flow import Flow, start, listen, or_

class MyFlow(Flow):
    @start()
    def fast_path(self):
        return "Fast result"

    @start()
    def slow_path(self):
        return "Slow result"

    @listen(or_(fast_path, slow_path))
    def handle_result(self, result):
        # Runs when either fast_path OR slow_path completes
        return f"Got: {result}"
```

### Label-Based Listening

Listen to router outputs by label:

```python
class MyFlow(Flow):
    @start()
    def process_request(self):
        if self.state.score > 80:
            return "approved"
        elif self.state.score > 50:
            return "revision"
        else:
            return "rejected"

    @listen("approved")
    def handle_approval(self):
        self.state.status = "approved"

    @listen("revision")
    def handle_revision(self):
        self.state.status = "needs_revision"

    @listen("rejected")
    def handle_rejection(self):
        self.state.status = "rejected"
```

### Data Passing

Methods receive return values from their listened sources:

```python
class MyFlow(Flow):
    @start()
    def gather_data(self):
        return {"key": "value", "number": 42}

    @listen(gather_data)
    def transform_data(self, data):
        # data = {"key": "value", "number": 42}
        return data["number"] * 2
```

---

## @router()

Conditionally routes execution based on return values.

### Basic Router

```python
from crewai.flow.flow import Flow, start, router, listen

class ReviewFlow(Flow):
    @start()
    def evaluate_content(self):
        score = self.calculate_score()
        self.state.score = score
        # Return label for routing
        if score >= 80:
            return "approved"
        elif score >= 50:
            return "revision"
        else:
            return "rejected"

    @router(evaluate_content)
    def route_decision(self, result):
        # Return the label directly
        return result

    @listen("approved")
    def publish_content(self):
        self.state.action = "published"
        return "Content published"

    @listen("revision")
    def request_changes(self):
        self.state.action = "revision_requested"
        return "Changes requested"

    @listen("rejected")
    def discard_content(self):
        self.state.action = "discarded"
        return "Content rejected"

    def calculate_score(self):
        return self.state.get("score", 0)
```

### Router with Dynamic Logic

```python
class DynamicFlow(Flow):
    @start()
    def analyze_input(self):
        intent = self.detect_intent()
        return intent  # "search", "create", "update", "delete"

    @router(analyze_input)
    def route_by_intent(self, intent):
        # Can add logic here before returning label
        if intent not in ["search", "create", "update", "delete"]:
            return "unknown"
        return intent

    @listen("search")
    def handle_search(self):
        return "Performing search..."

    @listen("create")
    def handle_create(self):
        return "Creating resource..."

    @listen("update")
    def handle_update(self):
        return "Updating resource..."

    @listen("delete")
    def handle_delete(self):
        return "Deleting resource..."

    @listen("unknown")
    def handle_unknown(self):
        return "Unknown action"

    def detect_intent(self):
        return self.state.get("intent", "unknown")
```

---

## @persist()

Saves flow state for recovery and resumption.

### Class-Level Persistence

Persists after every method execution:

```python
from crewai.flow.flow import Flow, start, listen, persist

@persist()
class PersistentFlow(Flow):
    @start()
    def step_one(self):
        self.state.progress = 0.25
        return "Step 1 done"

    @listen(step_one)
    def step_two(self):
        self.state.progress = 0.50
        return "Step 2 done"

    @listen(step_two)
    def step_three(self):
        self.state.progress = 0.75
        return "Step 3 done"

# State is automatically saved after each method
```

### Method-Level Persistence

Persist only specific methods:

```python
class SelectiveFlow(Flow):
    @start()
    def initialize(self):
        self.state.counter = 0
        return "Initialized"

    @persist()
    @listen(initialize)
    def critical_step(self):
        # Only this method triggers persistence
        self.state.counter += 1
        self.state.important_data = "saved"
        return "Critical work done"

    @listen(critical_step)
    def final_step(self):
        # No persistence after this
        return "Finished"
```

### State ID and Resume

```python
from crewai.flow.flow import Flow, start, listen, persist

@persist()
class ResumableFlow(Flow):
    @start()
    def load_data(self):
        # Access flow ID for tracking
        flow_id = self.state.id
        print(f"Flow ID: {flow_id}")
        
        self.state.data_loaded = True
        return "Data loaded"

    @listen(load_data)
    def process_data(self):
        self.state.processed = True
        return "Data processed"

# Resume a flow by ID
# flow = ResumableFlow()
# flow.resume(flow_id="previous-flow-id")
```

### Persistence Configuration

```python
from crewai.flow.persistence import SQLitePersistence

@persist(persistence=SQLitePersistence(db_path="./flows.db"))
class ConfiguredFlow(Flow):
    @start()
    def start_flow(self):
        self.state.start_time = datetime.now()
        return "Started"
```

---

## and_() / or_()

Utilities for combining multiple listeners.

### and_() - Fan-In

Wait for all sources:

```python
from crewai.flow.flow import Flow, start, listen, and_

class DataAggregationFlow(Flow):
    @start()
    def fetch_source_a(self):
        return {"source": "A", "data": [1, 2, 3]}

    @start()
    def fetch_source_b(self):
        return {"source": "B", "data": [4, 5, 6]}

    @start()
    def fetch_source_c(self):
        return {"source": "C", "data": [7, 8, 9]}

    @listen(and_(fetch_source_a, fetch_source_b, fetch_source_c))
    def aggregate_all(self, result_a, result_b, result_c):
        # Receives results from all three methods
        all_data = []
        all_data.extend(result_a["data"])
        all_data.extend(result_b["data"])
        all_data.extend(result_c["data"])
        return {"aggregated": all_data, "count": len(all_data)}
```

### or_() - Alternative Paths

Continue on first completion:

```python
from crewai.flow.flow import Flow, start, listen, or_

class RedundancyFlow(Flow):
    @start()
    def primary_api(self):
        if self.state.use_primary:
            return {"success": True, "data": "primary"}
        raise Exception("Primary failed")

    @start()
    def backup_api(self):
        if self.state.use_backup:
            return {"success": True, "data": "backup"}
        raise Exception("Backup failed")

    @listen(or_(primary_api, backup_api))
    def handle_response(self, response):
        # Runs when EITHER api succeeds
        if response["success"]:
            return f"Got data from {response['data']}"
        return "Both APIs failed"
```

### Combining and_ and or_

```python
class ComplexFlow(Flow):
    @start()
    def task_a(self):
        return "A"

    @start()
    def task_b(self):
        return "B"

    @start()
    def task_c(self):
        return "C"

    @listen(and_(task_a, or_(task_b, task_c)))
    def complex_condition(self, result_a, result_b_or_c):
        # task_a must complete AND (task_b OR task_c) must complete
        return f"Got A={result_a} and B/C={result_b_or_c}"
```

---

## Summary

| Decorator | Purpose | Key Parameters |
|-----------|---------|----------------|
| `@start()` | Entry point | `condition` (optional) |
| `@listen()` | Wait for completion | Source method(s) or label |
| `@router()` | Conditional routing | Source method |
| `@persist()` | State persistence | `persistence` (optional) |
| `and_()` | Fan-in (all must complete) | Multiple methods |
| `or_()` | Alternative (any can complete) | Multiple methods |
