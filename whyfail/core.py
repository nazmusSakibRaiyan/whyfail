"""
Core functionality for whyfail - context manager and decorator for error explanation.
"""
import traceback
import sys
from contextlib import contextmanager
from functools import wraps
from typing import Callable, Optional, Any
from .explainers import get_explainer


class ExplainerConfig:
    """Configuration for the explainer."""
    
    def __init__(
        self,
        show_traceback: bool = True,
        show_suggestions: bool = True,
        reraise: bool = True,
        suppress_standard_output: bool = False
    ):
        """
        Initialize explainer configuration.
        
        Args:
            show_traceback: Whether to show the full stack trace
            show_suggestions: Whether to show suggestions
            reraise: Whether to re-raise the exception after explaining
            suppress_standard_output: Whether to suppress regular exception output
        """
        self.show_traceback = show_traceback
        self.show_suggestions = show_suggestions
        self.reraise = reraise
        self.suppress_standard_output = suppress_standard_output


# Global configuration
_config = ExplainerConfig()


def configure(
    show_traceback: bool = True,
    show_suggestions: bool = True,
    reraise: bool = True,
    suppress_standard_output: bool = False
) -> None:
    """
    Configure global whyfail settings.
    
    Args:
        show_traceback: Whether to show the full stack trace
        show_suggestions: Whether to show suggestions
        reraise: Whether to re-raise the exception after explaining
        suppress_standard_output: Whether to suppress regular exception output
    """
    global _config
    _config = ExplainerConfig(
        show_traceback=show_traceback,
        show_suggestions=show_suggestions,
        reraise=reraise,
        suppress_standard_output=suppress_standard_output
    )


@contextmanager
def explain(
    show_traceback: Optional[bool] = None,
    show_suggestions: Optional[bool] = None,
    reraise: Optional[bool] = None,
    suppress_standard_output: Optional[bool] = None
):
    """
    Context manager to explain exceptions in a code block.
    
    This catches exceptions, looks them up in the explainer registry,
    and prints human-readable explanations instead of just stack traces.
    
    Args:
        show_traceback: Override global setting for showing traceback
        show_suggestions: Override global setting for showing suggestions
        reraise: Override global setting for reraising
        suppress_standard_output: Override global setting for suppressing output
    
    Example:
        >>> with whyfail.explain():
        ...     data["missing_key"]
        
        [WHYFAIL] Human-Readable Error Explanation
        ============================================================
        ❌ Missing dictionary key: missing_key
        ...
    
    Raises:
        The original exception if reraise=True (default)
    """
    # Determine configuration to use
    config = _config
    if any(arg is not None for arg in [show_traceback, show_suggestions, reraise, suppress_standard_output]):
        config = ExplainerConfig(
            show_traceback=show_traceback if show_traceback is not None else _config.show_traceback,
            show_suggestions=show_suggestions if show_suggestions is not None else _config.show_suggestions,
            reraise=reraise if reraise is not None else _config.reraise,
            suppress_standard_output=suppress_standard_output if suppress_standard_output is not None else _config.suppress_standard_output
        )
    
    try:
        yield
    except Exception as e:
        # Try to get an explainer for this exception type
        explainer = get_explainer(type(e))
        
        if explainer:
            try:
                explanation = explainer(e)
                print(explanation.format_output())
            except Exception as explain_err:
                # If explaining failed, show a generic message
                print(f"\n[WHYFAIL] Failed to explain error: {explain_err}\n")
        else:
            # No explainer found, show generic message
            print(f"\n[WHYFAIL] No explanation available for {type(e).__name__}\n")
        
        # Show traceback if configured
        if config.show_traceback:
            print("Full traceback:")
            print("-" * 60)
            traceback.print_exc()
            print("-" * 60)
        
        # Re-raise if configured
        if config.reraise:
            raise


def explain_errors(
    show_traceback: Optional[bool] = None,
    show_suggestions: Optional[bool] = None,
    reraise: Optional[bool] = None,
    suppress_standard_output: Optional[bool] = None
) -> Callable:
    """
    Decorator to explain exceptions in a function.
    
    Args:
        show_traceback: Whether to show the full stack trace
        show_suggestions: Whether to show suggestions
        reraise: Whether to re-raise the exception
        suppress_standard_output: Whether to suppress standard output
    
    Returns:
        Decorated function
    
    Example:
        >>> @whyfail.explain_errors()
        ... def risky_function():
        ...     return my_dict["key"]
        
        >>> risky_function()  # Will explain the KeyError
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with explain(
                show_traceback=show_traceback,
                show_suggestions=show_suggestions,
                reraise=reraise,
                suppress_standard_output=suppress_standard_output
            ):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def get_explanation(exc: Exception) -> Optional[str]:
    """
    Get the explanation for an exception without entering the context manager.
    
    Args:
        exc: The exception instance
    
    Returns:
        Formatted explanation string, or None if no explainer found
    
    Example:
        >>> try:
        ...     data["key"]
        ... except KeyError as e:
        ...     print(whyfail.get_explanation(e))
    """
    explainer = get_explainer(type(exc))
    if explainer:
        try:
            explanation = explainer(exc)
            return explanation.format_output()
        except Exception:
            return None
    return None
