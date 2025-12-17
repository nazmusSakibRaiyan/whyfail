# whyfail 🚀

**Make Python error messages understandable by humans, not just machines.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Stars](https://img.shields.io/github/stars/yourusername/whyfail?style=social)](https://github.com/yourusername/whyfail)

## The Problem

Ever seen this?

```
KeyError: 'user_id'
```

What do you do now?

- 🤔 Guess what went wrong?
- 📚 Google the error?
- 🤖 Ask ChatGPT?

## The Solution

**whyfail** explains what went wrong and how to fix it:

```python
import whyfail

with whyfail.explain():
    data["user_id"]  # KeyError
```

**Output:**

```
============================================================
[WHYFAIL] Human-Readable Error Explanation
============================================================
❌ Missing dictionary key: user_id

📌 Why this happened:
   You tried to access a dictionary key that doesn't exist.
   Dictionary keys are case-sensitive and must be initialized before access.

💡 How to fix it:
   1. Check if key 'user_id' is spelled correctly (case-sensitive)
   2. Print available keys using: dict.keys() or list(dict.keys())
   3. Initialize the key before accessing: dict['user_id'] = value
   4. Use dict.get('user_id', default_value) to avoid the error and return a default

🔍 Additional context:
   Attempted key: user_id
============================================================
```

## Features ✨

✅ **Context Manager** - Wrap code blocks to explain errors  
✅ **Decorator** - Add to functions for automatic error explanation  
✅ **9 Common Exceptions** - KeyError, IndexError, TypeError, ValueError, and more  
✅ **Pluggable System** - Add custom explanations for your own exceptions  
✅ **Zero Magic** - No monkey-patching, fully transparent  
✅ **Easy Configuration** - Control verbosity and output  
✅ **Educational** - Perfect for teaching Python  

## Installation

```bash
pip install whyfail
```

Or from source:

```bash
git clone https://github.com/yourusername/whyfail.git
cd whyfail
pip install -e .
```

## Quick Start

### Option 1: Context Manager (Best for quick debugging)

```python
import whyfail

with whyfail.explain():
    my_list = [1, 2, 3]
    print(my_list[10])  # IndexError: list index out of range
```

**Output:**
```
============================================================
[WHYFAIL] Human-Readable Error Explanation
============================================================
❌ List index out of range

📌 Why this happened:
   You tried to access an element at an index that doesn't exist in a list...

💡 How to fix it:
   1. Check the length of your list/string: len(my_list)
   2. Remember: index 0 is the FIRST element, index len(list)-1 is the LAST
   ...
============================================================
```

### Option 2: Decorator (Best for functions)

```python
import whyfail

@whyfail.explain_errors()
def parse_json(data):
    return int(data)

parse_json("not a number")  # ValueError: invalid literal for int()
```

**Benefits:** Automatically explains errors in the function without wrapping each call.

### Option 3: Manual Explanation (Best for custom error handling)

```python
import whyfail

try:
    result = 10 / 0
except ZeroDivisionError as e:
    explanation = whyfail.get_explanation(e)
    log.error(explanation)  # Log the human-readable explanation
    notify_user("Math error occurred")
```

**Perfect for:** Custom error handling, logging systems, API responses.

## Supported Exceptions (v0.1.0)

| Exception | Explanation |
|-----------|-------------|
| `KeyError` | Missing dictionary key with suggestions for close matches |
| `IndexError` | List/string index out of range with bounds checking tips |
| `TypeError` | Wrong data type for operation with conversion hints |
| `ValueError` | Invalid value format with validation examples |
| `AttributeError` | Object has no attribute with alternative suggestions |
| `NameError` | Variable not defined with scope guidance |
| `ZeroDivisionError` | Division by zero with prevention strategies |
| `FileNotFoundError` | File path issues with debugging steps |
| `ImportError` | Module import issues with troubleshooting steps |

## Configuration

### Global Configuration

```python
import whyfail

# Configure defaults for all explain() calls
whyfail.configure(
    show_traceback=True,        # Show full stack trace
    show_suggestions=True,      # Show actionable suggestions
    reraise=True,              # Re-raise exception after explaining
    suppress_standard_output=False
)
```

### Per-Call Configuration

```python
with whyfail.explain(show_traceback=False, reraise=False):
    risky_operation()
```

## Custom Explainers

Add explanations for your own exceptions:

```python
import whyfail
from whyfail import Explanation

class CustomError(Exception):
    pass

def explain_custom_error(err: CustomError) -> Explanation:
    return Explanation(
        title="My custom error occurred",
        reason="You did something I don't like",
        suggestions=[
            "Do this instead",
            "Or try that approach"
        ]
    )

whyfail.register_explainer(CustomError, explain_custom_error)

# Now your custom errors are explained too!
with whyfail.explain():
    raise CustomError("oops")
```

## API Reference

### `whyfail.explain()`

Context manager that catches and explains exceptions.

```python
with whyfail.explain(show_traceback=True, reraise=True):
    # Your code here
```

**Parameters:**
- `show_traceback` (bool): Show full stack trace (default: True)
- `show_suggestions` (bool): Show suggestions (default: True)
- `reraise` (bool): Re-raise exception after explaining (default: True)
- `suppress_standard_output` (bool): Suppress output (default: False)

### `@whyfail.explain_errors()`

Decorator for automatic error explanation in functions.

```python
@whyfail.explain_errors(show_traceback=False)
def my_function():
    pass
```

### `whyfail.configure()`

Set global configuration for all explain() calls.

```python
whyfail.configure(show_traceback=False, reraise=False)
```

### `whyfail.get_explanation(exception)`

Get explanation without entering context manager.

```python
try:
    risky()
except KeyError as e:
    explanation = whyfail.get_explanation(e)
    print(explanation)
```

### `whyfail.register_explainer(exception_type, explainer_func)`

Register custom explainer for your exception type.

```python
whyfail.register_explainer(MyError, my_explainer_function)
```

## Use Cases 🎯

### 1. **Teaching Python to Beginners**
Help students understand *why* errors happen, not just *that* they happen.

```python
# Instead of showing stack traces, show explanations
import whyfail

@whyfail.explain_errors(show_traceback=False, reraise=False)
def student_exercise(data):
    return data["age"] + 10

# Student gets helpful feedback without scary stack trace
student_exercise({"name": "Alice"})
```

**Why it helps:** Beginners see what went wrong and how to fix it, building confidence instead of frustration.

---

### 2. **Learning Platforms & Online Judges**
Provide immediate, helpful feedback in coding exercises.

```python
# exercise_feedback.py
import whyfail

def grade_exercise(student_code):
    whyfail.configure(show_traceback=False, reraise=False)
    
    try:
        with whyfail.explain():
            exec(student_code)
        return {"status": "passed"}
    except Exception as e:
        explanation = whyfail.get_explanation(e)
        return {
            "status": "failed",
            "hint": explanation,
            "message": "See explanation above"
        }
```

**Use in:** Jupyter notebooks, online IDEs, coding challenge platforms.

---

### 3. **Debugging During Development**
Understand complex errors faster during development.

```python
import whyfail
import json

def load_config(filepath):
    with whyfail.explain(show_traceback=True):  # Show full trace for debugging
        with open(filepath) as f:
            config = json.load(f)
        return config

# If something fails, you get both:
# - Human-readable explanation
# - Full traceback for investigation
load_config("config.json")
```

**Use in:** Development, testing, rapid debugging.

---

### 4. **Production Error Logging**
Log errors in a way that developers can understand and fix.

```python
import whyfail
import logging

logger = logging.getLogger(__name__)

def process_data(user_data):
    try:
        # Business logic...
        return int(user_data["age"])
    except Exception as e:
        # Log the human-readable explanation
        explanation = whyfail.get_explanation(e)
        logger.error(f"Processing failed:\n{explanation}")
        # Also log for monitoring/alerting
        sentry.capture_exception(e)
        raise

# Developers reading logs see actionable explanations
```

**Benefits:**
- Faster incident response
- Easier debugging from logs
- Self-documenting error behavior

---

### 5. **API Error Responses**
Return helpful error messages to API clients.

```python
from fastapi import FastAPI, HTTPException
import whyfail

app = FastAPI()

@app.post("/process")
def process(data: dict):
    with whyfail.explain(reraise=False):
        result = data["user_id"] + 10
        return {"result": result}

# If KeyError: client gets helpful explanation instead of 500 error
# More helpful than: {"detail": "KeyError: 'user_id'"}
```

---

### 6. **Educational Tools & Tutoring**
Build tools that teach programming concepts.

```python
import whyfail

class PythonTutor:
    def run_student_code(self, code_string):
        whyfail.configure(show_traceback=False, reraise=False)
        
        with whyfail.explain():
            exec(code_string)
        
        print("✅ Code ran successfully!")
```

**Ideal for:** Chatbots, tutoring platforms, educational apps.

---

### 7. **Debugging Tests**
Make test failures more understandable.

```python
import pytest
import whyfail

@pytest.fixture
def explain_errors():
    return whyfail.explain(show_traceback=True, reraise=True)

def test_user_creation():
    with whyfail.explain():
        user = {"name": "Alice"}
        age = user["age"]  # KeyError with helpful explanation
```

---

## Real-World Comparison

### Without whyfail ❌
```
KeyError: 'user_id'
Traceback (most recent call last):
  File "app.py", line 45, in process_user
    user_id = data["user_id"]
KeyError: 'user_id'
```

**What the developer does:**
- 😕 "Why is this key missing?"
- 🔍 Searches Google
- ⏱️ Wastes 10 minutes debugging

### With whyfail ✅
```
============================================================
[WHYFAIL] Human-Readable Error Explanation
============================================================
❌ Missing dictionary key: user_id

📌 Why this happened:
   You tried to access a dictionary key that doesn't exist...

💡 How to fix it:
   1. Check if key 'user_id' is spelled correctly (case-sensitive)
   2. Print available keys using: dict.keys()
   3. Initialize the key before accessing...

🔍 Additional context:
   Attempted key: user_id
============================================================
```

**What the developer does:**
- ✨ Reads explanation
- 🎯 Understands the issue
- ✅ Fixes it in 30 seconds

---

## Examples

Check the `examples/` directory for complete working examples:

- [basic_usage.py](examples/basic_usage.py) - Simple examples of all error types
- [teaching_mode.py](examples/teaching_mode.py) - Educational configuration
- [custom_explainers.py](examples/custom_explainers.py) - Creating custom explanations
- [integration_example.py](examples/integration_example.py) - Integrating with your app

## Testing

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=whyfail
```

## Roadmap 🗺️

### v0.2.0 (Planned)
- [ ] More exception types (ImportError, AttributeError improvements)
- [ ] Stack trace parsing for context
- [ ] Suggestion ranking by relevance

### v0.3.0 (Planned)
- [ ] IDE integration (VS Code, PyCharm plugins)
- [ ] AI-powered explanations (optional, not required)
- [ ] Multi-language support

### v1.0.0 (Vision)
- [ ] Production-ready with extensive testing
- [ ] Performance optimizations
- [ ] Official IDE plugins

## Contributing 🤝

We love contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Submit a pull request

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/whyfail.git
cd whyfail

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black whyfail tests
isort whyfail tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Inspired by:
- Error messages in Rust and Elm (which explain errors beautifully)
- The frustration of cryptic Python error messages
- The educational community's need for clearer feedback

## Questions?

- 📖 [Full Documentation](https://github.com/yourusername/whyfail/wiki)
- 🐛 [Report Issues](https://github.com/yourusername/whyfail/issues)
- 💬 [Discussions](https://github.com/yourusername/whyfail/discussions)

---

**Made with ❤️ for the Python community**
