"""
whyfail - Human-readable Error Explainer for Python

Make error messages understandable by humans, not just machines.

Example:
    >>> import whyfail
    >>> with whyfail.explain():
    ...     data["missing_key"]
    
    [WHYFAIL] Human-Readable Error Explanation
    ============================================================
    ❌ Missing dictionary key: missing_key
    📌 Why this happened:
       You tried to access a dictionary key that doesn't exist...
    💡 How to fix it:
       1. Check if key 'missing_key' is spelled correctly (case-sensitive)
       ...
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__license__ = "MIT"

from .core import explain, explain_errors, configure, get_explanation
from .explainers import register_explainer, get_explainer
from .models import Explanation

__all__ = [
    "explain",
    "explain_errors",
    "configure",
    "get_explanation",
    "register_explainer",
    "get_explainer",
    "Explanation",
]
