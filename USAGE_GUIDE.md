# whyfail Usage Guide

**Making Python errors human-friendly, one exception at a time.**

This guide shows you exactly how to use whyfail in your real-world projects.

---

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [API Overview](#api-overview)
3. [Common Patterns](#common-patterns)
4. [Real-World Examples](#real-world-examples)
5. [Best Practices](#best-practices)

---

## Core Concepts

### The Problem

Python errors are written for machines:

```
KeyError: 'user_id'
```

Humans have to:
- Google the error
- Debug the code
- Guess what went wrong

### The Solution

**whyfail explains what happened AND how to fix it:**

```
[WHYFAIL] Missing dictionary key: user_id
Why: You tried to access a dict key that doesn't exist
How to fix:
  1. Check spelling of 'user_id' (case-sensitive)
  2. Print dict.keys() to see available keys
  3. Initialize the key before accessing
```

---

## API Overview

### 1. Context Manager: `with whyfail.explain():`

Wraps a block of code and catches exceptions.

```python
import whyfail

with whyfail.explain():
    # Your code here
    data["missing_key"]
```

**Parameters:**
- `show_traceback` (bool): Show full Python traceback (default: True)
- `reraise` (bool): Re-raise exception after explaining (default: True)

**When to use:** Quick debugging, short code blocks.

---

### 2. Decorator: `@whyfail.explain_errors()`

Wraps a function to catch and explain errors automatically.

```python
import whyfail

@whyfail.explain_errors()
def my_function(data):
    return data["key"]
```

**When to use:** Functions that might fail, automatic error handling.

---

### 3. Manual: `whyfail.get_explanation(exception)`

Get explanation without entering context manager.

```python
import whyfail

try:
    risky_operation()
except KeyError as e:
    explanation = whyfail.get_explanation(e)
    print(explanation)
```

**When to use:** Custom error handling, logging, API responses.

---

### 4. Configuration: `whyfail.configure()`

Set global defaults for all explain() calls.

```python
import whyfail

# Teaching mode: no traceback, no re-raise
whyfail.configure(show_traceback=False, reraise=False)

# Development mode: show everything
whyfail.configure(show_traceback=True, reraise=True)
```

---

## Common Patterns

### Pattern 1: Debug a Single Function

```python
import whyfail

@whyfail.explain_errors()
def load_user_data(user_id):
    users = [{"id": 1, "name": "Alice"}]
    return users[user_id]  # IndexError

# Run it
load_user_data(999)  # Explains IndexError with helpful suggestions
```

---

### Pattern 2: Wrap Risky Code Block

```python
import whyfail

with whyfail.explain():
    # If any error happens, it's explained
    config = json.load(open("config.json"))
    age = config["user"]["age"]
    print(10 / age)
```

---

### Pattern 3: Custom Error Handling in Loops

```python
import whyfail

records = [{"name": "Alice"}, {"name": "Bob", "age": 25}]

for record in records:
    with whyfail.explain(reraise=False):  # Don't stop the loop
        print(f"{record['name']} is {record['age']} years old")
```

**Output:**
```
[WHYFAIL] Missing dictionary key: age
...
Bob is 25 years old
```

---

### Pattern 4: Testing with Helpful Errors

```python
import whyfail
import pytest

def test_user_creation():
    with whyfail.explain():
        user = create_user({"name": "Alice"})
        assert user["id"] is not None  # Helpful if creation fails
```

---

### Pattern 5: Logging Errors Intelligently

```python
import whyfail
import logging

logger = logging.getLogger(__name__)

try:
    process_payment(user_data)
except Exception as e:
    explanation = whyfail.get_explanation(e)
    if explanation:
        logger.error(f"Payment failed:\n{explanation}")
    else:
        logger.error(f"Unknown error: {e}", exc_info=True)
```

---

## Real-World Examples

### Example 1: Web API (FastAPI)

```python
from fastapi import FastAPI
import whyfail

app = FastAPI()

@app.post("/users")
def create_user(data: dict):
    with whyfail.explain(show_traceback=False, reraise=False):
        user = {
            "id": len(users) + 1,
            "name": data["name"],      # KeyError if missing
            "age": int(data["age"])     # ValueError if not a number
        }
        users.append(user)
        return user
```

**Client sees:**
- Helpful error messages
- Actionable suggestions
- No scary stack traces

---

### Example 2: Data Processing Pipeline

```python
import whyfail
import pandas as pd

whyfail.configure(show_traceback=True, reraise=False)

def process_csv(filepath):
    with whyfail.explain():
        df = pd.read_csv(filepath)
        df["age"] = df["age"].astype(int)
        df["email"] = df["email"].str.lower()
        return df

# Run on multiple files
for file in ["users.csv", "customers.csv"]:
    try:
        result = process_csv(file)
        print(f"✅ {file} processed")
    except Exception:
        print(f"❌ {file} failed")
```

---

### Example 3: Teaching Python

```python
import whyfail

# Configure for students: show explanation, no traceback, no re-raise
whyfail.configure(
    show_traceback=False,
    show_suggestions=True,
    reraise=False
)

print("=" * 60)
print("Python Error Explanation Tutorial")
print("=" * 60)

print("\n1. KeyError Example:")
with whyfail.explain():
    data = {"name": "Alice"}
    print(data["age"])

print("\n2. IndexError Example:")
with whyfail.explain():
    numbers = [1, 2, 3]
    print(numbers[10])

print("\n3. TypeError Example:")
with whyfail.explain():
    result = "hello" + 5
    print(result)

print("\n" + "=" * 60)
print("Now you understand common Python errors!")
```

---

### Example 4: Testing with whyfail

```python
import pytest
import whyfail
from myapp import get_user, process_order

class TestAPI:
    def test_get_user_missing_id(self):
        """Error should be helpful."""
        with whyfail.explain():
            # If get_user fails, error is explained
            user = get_user(id=999)
    
    def test_process_order_invalid_data(self):
        """Integration test with helpful errors."""
        with whyfail.explain(show_traceback=True):
            order = process_order({
                "user_id": "invalid",  # Should be int
                "items": ["item1"]
            })
```

---

### Example 5: CLI Tool with Error Handling

```python
#!/usr/bin/env python3
import whyfail
import click
import json

whyfail.configure(show_traceback=False, reraise=False)

@click.command()
@click.argument('filename')
def process_file(filename):
    """Process a JSON file."""
    with whyfail.explain():
        with open(filename) as f:
            data = json.load(f)
        
        # Process data...
        result = data["users"][0]["email"]
        click.echo(f"Processed: {result}")

if __name__ == "__main__":
    try:
        process_file()
    except SystemExit:
        pass  # Let Click handle exit codes
```

---

### Example 6: Database Operations

```python
import whyfail
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///users.db")

def get_user_email(user_id):
    with whyfail.explain(show_traceback=False):
        with Session(engine) as session:
            user = session.query(User).filter(User.id == user_id).first()
            return user.email  # AttributeError if user is None
```

---

## Best Practices

### ✅ DO

**1. Use context manager for debugging**
```python
with whyfail.explain():
    risky_code()
```

**2. Use decorator for functions**
```python
@whyfail.explain_errors()
def my_function():
    pass
```

**3. Use manual explanation for logging**
```python
except Exception as e:
    explanation = whyfail.get_explanation(e)
    log.error(explanation)
```

**4. Configure for your use case**
```python
# Teaching mode
whyfail.configure(show_traceback=False, reraise=False)

# Production mode
whyfail.configure(show_traceback=True, reraise=True)
```

---

### ❌ DON'T

**1. Don't suppress all errors**
```python
# Bad: This hides real issues
with whyfail.explain(reraise=False):
    entire_application()
```

**2. Don't use in tight loops without consideration**
```python
# Inefficient: Adds overhead
for i in range(1000000):
    with whyfail.explain():
        process(i)
```

**3. Don't forget to handle the exception**
```python
# Bad: Exception still occurs after explaining
with whyfail.explain():
    risky()
# Program continues? No, it raises!
```

**4. Don't rely on whyfail for control flow**
```python
# Bad: Don't use exceptions for normal logic
with whyfail.explain(reraise=False):
    if key in data:
        value = data[key]
```

---

## Troubleshooting

### Q: Error isn't being explained?
**A:** whyfail supports 9 common exceptions. For custom exceptions, register an explainer:

```python
import whyfail

class MyError(Exception):
    pass

def explain_my_error(err):
    return whyfail.Explanation(
        title="My custom error",
        reason="Here's why it happened",
        suggestions=["Try this", "Or this"]
    )

whyfail.register_explainer(MyError, explain_my_error)
```

---

### Q: I see traceback but I don't want it?
**A:** Use `show_traceback=False`:

```python
with whyfail.explain(show_traceback=False):
    code()
```

Or configure globally:

```python
whyfail.configure(show_traceback=False)
```

---

### Q: Exception isn't being re-raised?
**A:** Use `reraise=True`:

```python
with whyfail.explain(reraise=True):  # Default behavior
    code()
```

---

### Q: How do I use whyfail in production?
**A:** Use manual explanation for logging:

```python
try:
    operation()
except Exception as e:
    explanation = whyfail.get_explanation(e)
    log.error(explanation)
    sentry.capture_exception(e)
```

---

## Summary

| Use Case | Recommended API | Example |
|----------|-----------------|---------|
| **Quick debugging** | Context manager | `with whyfail.explain():` |
| **Function errors** | Decorator | `@whyfail.explain_errors()` |
| **Custom handling** | Manual explanation | `whyfail.get_explanation(e)` |
| **Global config** | configure() | `whyfail.configure(...)` |

**Start using whyfail today and make Python errors understandable!** 🚀
