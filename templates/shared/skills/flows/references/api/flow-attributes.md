# Flow Class Attributes Reference

## Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `state` | `BaseModel` \| `dict` | - | Current flow state containing all data passed between methods |
| `id` | `str` | UUID | Unique flow identifier auto-generated on initialization |
| `_listeners` | `dict` | `{}` | Registered listeners mapping source methods to target methods |
| `_routers` | `dict` | `{}` | Registered routers for conditional execution paths |
| `_methods` | `list` | `[]` | List of all flow methods decorated with `@start`, `@listen`, or `@router` |

---

## Attribute Details

### state

The central data store for the flow.

```python
from crewai.flow.flow import Flow, start, listen
from pydantic import BaseModel

# Unstructured state (dict-like)
class DictFlow(Flow):
    @start()
    def example(self):
        # Access state as dictionary
        self.state["key"] = "value"
        value = self.state.get("key")
        return value

# Structured state (Pydantic)
class MyState(BaseModel):
    count: int = 0
    message: str = ""

class TypedFlow(Flow[MyState]):
    @start()
    def example(self):
        # Access state with type safety
        self.state.count += 1
        self.state.message = f"Count is {self.state.count}"
        return self.state
```

### id

Unique identifier for the flow instance.

```python
class IdExampleFlow(Flow):
    @start()
    def show_id(self):
        # Access flow ID
        flow_id = self.id
        
        # Also available in state
        state_id = self.state.id  # Structured
        # or
        state_id = self.state["id"]  # Unstructured
        
        print(f"Flow ID: {flow_id}")
        return flow_id
```

### _listeners

Internal registry of listener relationships.

```python
from crewai.flow.flow import Flow, start, listen

class ListenerFlow(Flow):
    @start()
    def source_method(self):
        return "source"

    @listen(source_method)
    def target_method(self, data):
        return f"received: {data}"

# The _listeners dict contains:
# {
#     source_method: [target_method]
# }
```

### _routers

Internal registry of router relationships.

```python
from crewai.flow.flow import Flow, start, router, listen

class RouterFlow(Flow):
    @start()
    def decide(self):
        return "path_a" if self.state.condition else "path_b"

    @router(decide)
    def route(self, decision):
        return decision

    @listen("path_a")
    def handle_a(self):
        return "Path A"

    @listen("path_b")
    def handle_b(self):
        return "Path B"

# The _routers dict contains:
# {
#     decide: route
# }
```

### _methods

List of all decorated flow methods.

```python
from crewai.flow.flow import Flow, start, listen

class MethodTrackingFlow(Flow):
    @start()
    def method_a(self):
        return "A"

    @listen(method_a)
    def method_b(self, data):
        return f"B received: {data}"

    @listen(method_b)
    def method_c(self, data):
        return f"C received: {data}"

# The _methods list contains references to:
# [method_a, method_b, method_c]
```

---

## Methods

### kickoff()

Starts flow execution from all `@start` methods.

**Signature:**
```python
def kickoff(self, inputs: Optional[dict] = None) -> Any
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `inputs` | `dict` | `None` | Optional initial values for state |

**Returns:**
Results from the final methods in the flow execution.

**Example:**
```python
from crewai.flow.flow import Flow, start, listen

class SimpleFlow(Flow):
    @start()
    def step_one(self):
        self.state.value = 1
        return "Step 1"

    @listen(step_one)
    def step_two(self, prev):
        self.state.value = 2
        return "Step 2"

# Execute the flow
flow = SimpleFlow()
result = flow.kickoff()
print(result)  # "Step 2"
print(flow.state.value)  # 2
```

**With initial inputs:**
```python
class InputFlow(Flow):
    @start()
    def initialize(self):
        # Access inputs via state
        name = self.state.get("user_name", "Anonymous")
        return f"Hello, {name}"

flow = InputFlow()
result = flow.kickoff(inputs={"user_name": "Alice"})
print(result)  # "Hello, Alice"
```

---

### kickoff_async()

Asynchronously starts flow execution.

**Signature:**
```python
async def kickoff_async(self, inputs: Optional[dict] = None) -> Any
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `inputs` | `dict` | `None` | Optional initial values for state |

**Returns:**
Awaitable results from the final methods.

**Example:**
```python
import asyncio
from crewai.flow.flow import Flow, start, listen

class AsyncFlow(Flow):
    @start()
    async def async_step(self):
        await asyncio.sleep(1)
        self.state.done = True
        return "Async complete"

async def main():
    flow = AsyncFlow()
    result = await flow.kickoff_async()
    print(result)  # "Async complete"

asyncio.run(main())
```

**Mixed sync/async flow:**
```python
class MixedFlow(Flow):
    @start()
    def sync_step(self):
        return "Sync result"

    @listen(sync_step)
    async def async_step(self, data):
        await asyncio.sleep(0.1)
        return f"Async: {data}"

# Both kickoff() and kickoff_async() work
```

---

### plot()

Generates a visualization of the flow structure.

**Signature:**
```python
def plot(self, filename: Optional[str] = None) -> None
```

**Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `filename` | `str` | `None` | Output filename (default: flow_plot.html) |

**Returns:**
None (generates visualization file)

**Example:**
```python
from crewai.flow.flow import Flow, start, listen, router

class VisualFlow(Flow):
    @start()
    def start_node(self):
        return "start"

    @listen(start_node)
    def middle_node(self, data):
        return data

    @listen(middle_node)
    def end_node(self, data):
        return data

flow = VisualFlow()
flow.plot("my_flow.html")  # Creates my_flow.html visualization
```

**Visualizes:**
- Start methods (entry points)
- Listen relationships (edges)
- Router branches
- Method execution order

---

## Complete Example

```python
from crewai.flow.flow import Flow, start, listen, router, and_
from pydantic import BaseModel
from typing import Any

class OrderState(BaseModel):
    id: str
    items: list = []
    total: float = 0.0
    status: str = "pending"

class OrderFlow(Flow[OrderState]):
    """
    Complete flow demonstrating all attributes and methods.
    """

    def __init__(self):
        super().__init__()
        # Initialize with any custom setup
        self._custom_config = {"tax_rate": 0.08}

    @start()
    def validate_items(self):
        """Entry point - validates order items."""
        if not self.state.items:
            return "invalid"
        return "valid"

    @router(validate_items)
    def route_validation(self, result):
        """Routes based on validation result."""
        return result

    @listen("invalid")
    def handle_invalid(self):
        """Handle invalid order."""
        self.state.status = "rejected"
        return {"error": "No items in order"}

    @listen("valid")
    def calculate_total(self):
        """Calculate order total with tax."""
        subtotal = sum(item["price"] for item in self.state.items)
        tax = subtotal * self._custom_config["tax_rate"]
        self.state.total = subtotal + tax
        return self.state.total

    @listen(calculate_total)
    def confirm_order(self, total):
        """Finalize order."""
        self.state.status = "confirmed"
        return {
            "order_id": self.state.id,
            "total": total,
            "status": self.state.status
        }

# Usage example
if __name__ == "__main__":
    # Create flow instance
    flow = OrderFlow()
    
    # Set initial state
    initial_state = {
        "id": flow.id,
        "items": [
            {"name": "Widget", "price": 29.99},
            {"name": "Gadget", "price": 49.99}
        ]
    }
    
    # Execute flow
    result = flow.kickoff(inputs=initial_state)
    
    print(f"Flow ID: {flow.id}")
    print(f"Final State: {flow.state}")
    print(f"Result: {result}")
    
    # Generate visualization
    flow.plot("order_flow.html")
```

---

## Summary Table

### Attributes

| Attribute | Access | Purpose |
|-----------|--------|---------|
| `state` | `self.state` | Data storage and transmission |
| `id` | `self.id` | Unique flow identification |
| `_listeners` | `self._listeners` | Internal: listener registry |
| `_routers` | `self._routers` | Internal: router registry |
| `_methods` | `self._methods` | Internal: method registry |

### Methods

| Method | Purpose | Sync/Async |
|--------|---------|------------|
| `kickoff()` | Start execution | Sync |
| `kickoff_async()` | Start execution | Async |
| `plot()` | Generate visualization | Sync |
