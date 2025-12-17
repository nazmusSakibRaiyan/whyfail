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

### Option 1: Context Manager

```python
import whyfail

with whyfail.explain():
    my_list = [1, 2, 3]
    print(my_list[10])  # IndexError: list index out of range
```

### Option 2: Decorator

```python
import whyfail

@whyfail.explain_errors()
def parse_json(data):
    return int(data)

parse_json("not a number")  # ValueError: invalid literal for int()
```

### Option 3: Manual Explanation

```python
import whyfail

try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(whyfail.get_explanation(e))
```

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

### 1. **Teaching Python**
```python
# Help students understand common mistakes
with whyfail.explain():
    student_code()
```

### 2. **Learning Platforms**
```python
# Automatically explain errors in exercise feedback
@whyfail.explain_errors()
def run_student_submission(code):
    exec(code)
```

### 3. **Debugging**
```python
# Understand errors during development
with whyfail.explain(show_traceback=True):
    my_complex_function()
```

### 4. **Error Logging**
```python
# Custom error reporting
try:
    operation()
except Exception as e:
    log.error(whyfail.get_explanation(e))
```

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
