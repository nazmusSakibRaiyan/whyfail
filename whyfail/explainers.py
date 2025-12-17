"""
Error explainers that map exception types to human-readable explanations.
"""
from typing import Callable, Dict, Optional, Type
from .models import Explanation
from .utils import get_dict_suggestions, format_value


def explain_key_error(err: KeyError) -> Explanation:
    """
    Explain a KeyError exception.
    
    Args:
        err: The KeyError instance
    
    Returns:
        Human-readable explanation
    """
    key = err.args[0] if err.args else "unknown"
    return Explanation(
        title=f"Missing dictionary key: {key}",
        reason="You tried to access a dictionary key that doesn't exist. "
                "Dictionary keys are case-sensitive and must be initialized before access.",
        suggestions=[
            f"Check if key '{key}' is spelled correctly (case-sensitive)",
            "Print available keys using: dict.keys() or list(dict.keys())",
            f"Initialize the key before accessing: dict['{key}'] = value",
            "Use dict.get('{key}', default_value) to avoid the error and return a default"
        ],
        context=f"Attempted key: {format_value(key)}"
    )


def explain_index_error(err: IndexError) -> Explanation:
    """
    Explain an IndexError exception.
    
    Args:
        err: The IndexError instance
    
    Returns:
        Human-readable explanation
    """
    return Explanation(
        title="List index out of range",
        reason="You tried to access an element at an index that doesn't exist in a list, "
                "tuple, or string. Remember: indexing starts at 0, and the last valid index is len(sequence) - 1.",
        suggestions=[
            "Check the length of your list/string: len(my_list)",
            "Remember: index 0 is the FIRST element, index len(list)-1 is the LAST",
            "Use negative indexing for the end: list[-1] for last, list[-2] for second-to-last",
            "Add bounds checking: if index < len(my_list): value = my_list[index]",
            "Use a for loop instead: for item in my_list: (no index needed)"
        ],
        context="The index you tried to access was beyond the size of the sequence"
    )


def explain_type_error(err: TypeError) -> Explanation:
    """
    Explain a TypeError exception.
    
    Args:
        err: The TypeError instance
    
    Returns:
        Human-readable explanation
    """
    err_msg = str(err)
    return Explanation(
        title="Operation not supported for this data type",
        reason="You tried to perform an operation (like addition, function call, or indexing) "
                "on data of the wrong type. Python is strict about operations between incompatible types.",
        suggestions=[
            "Check the data type: type(variable)",
            "Convert types explicitly: int(x), str(x), float(x), list(x)",
            "For string concatenation, use: str(x) + str(y) (not x + y if x or y is a number)",
            "For function arguments, ensure you're passing the correct type",
            f"Error details: {err_msg}"
        ],
        context="Ensure all operands have compatible types for the operation"
    )


def explain_value_error(err: ValueError) -> Explanation:
    """
    Explain a ValueError exception.
    
    Args:
        err: The ValueError instance
    
    Returns:
        Human-readable explanation
    """
    err_msg = str(err)
    return Explanation(
        title="Invalid value for this operation",
        reason="You passed a value that exists and has the right type, but its content "
                "is invalid for the operation. For example, trying to convert 'hello' to an integer.",
        suggestions=[
            f"Check the value being used. Error: {err_msg}",
            "For int/float conversion: Use try-except or validate first",
            "Validate input data before processing: if x.isdigit(): value = int(x)",
            "For parsing, print the exact value being parsed: print(repr(value))",
            "Use string methods to check format: str.isdigit(), str.isalpha(), etc."
        ],
        context="The value exists but doesn't match expected format or constraints"
    )


def explain_attribute_error(err: AttributeError) -> Explanation:
    """
    Explain an AttributeError exception.
    
    Args:
        err: The AttributeError instance
    
    Returns:
        Human-readable explanation
    """
    err_msg = str(err)
    return Explanation(
        title="Object has no such attribute or method",
        reason="You tried to access an attribute or method that doesn't exist on an object. "
                "This often happens with typos, importing the wrong module, or using the wrong data type.",
        suggestions=[
            "Check the spelling of the attribute/method name (case-sensitive)",
            "Print available attributes: dir(object)",
            "Check what type the object actually is: type(object)",
            "Ensure you imported the right module: import module; help(module)",
            "Verify you didn't accidentally shadow a variable name",
            f"Error details: {err_msg}"
        ],
        context="Use dir(object) to see what attributes/methods are available"
    )


def explain_name_error(err: NameError) -> Explanation:
    """
    Explain a NameError exception.
    
    Args:
        err: The NameError instance
    
    Returns:
        Human-readable explanation
    """
    err_msg = str(err)
    return Explanation(
        title="Variable or function is not defined",
        reason="You tried to use a variable, function, or class that was never created or assigned. "
                "This is usually due to a typo, or the variable is defined in a different scope.",
        suggestions=[
            "Check the spelling of the variable name (case-sensitive)",
            "Make sure you assigned the variable before using it: x = 5",
            "If it's a function, ensure it's imported: from module import function",
            "Check if the variable is defined in the right scope (indentation, function body)",
            "Print all defined variables: print(dir()) in the current scope",
            f"Error details: {err_msg}"
        ],
        context="Variables must be defined before use"
    )


def explain_zero_division_error(err: ZeroDivisionError) -> Explanation:
    """
    Explain a ZeroDivisionError exception.
    
    Args:
        err: The ZeroDivisionError instance
    
    Returns:
        Human-readable explanation
    """
    return Explanation(
        title="Cannot divide by zero",
        reason="Mathematical operations cannot divide a number by zero. "
                "This is undefined in mathematics and will always cause an error.",
        suggestions=[
            "Check your divisor: if divisor != 0: result = numerator / divisor",
            "Use a default value: result = numerator / divisor if divisor != 0 else 0",
            "Use try-except: try: result = x / y except ZeroDivisionError: result = None",
            "For modulo (%), also check: if divisor != 0: result = x % y",
            "Add validation: validate that inputs won't cause zero division"
        ],
        context="Always ensure the divisor is non-zero before division"
    )


def explain_file_not_found_error(err: FileNotFoundError) -> Explanation:
    """
    Explain a FileNotFoundError exception.
    
    Args:
        err: The FileNotFoundError instance
    
    Returns:
        Human-readable explanation
    """
    err_msg = str(err)
    return Explanation(
        title="File not found",
        reason="You tried to open or access a file that doesn't exist at the specified path. "
                "This could be a typo in the filename, wrong directory, or the file was deleted.",
        suggestions=[
            "Check the file path is correct: print(filepath)",
            "Use absolute paths instead of relative: os.path.abspath(filepath)",
            "Check file exists: import os; os.path.exists(filepath)",
            "List files in directory: os.listdir(directory_path)",
            "Ensure working directory is correct: os.getcwd()",
            f"Error details: {err_msg}"
        ],
        context="Verify the file exists and the path is correct"
    )


def explain_import_error(err: ImportError) -> Explanation:
    """
    Explain an ImportError exception.
    
    Args:
        err: The ImportError instance
    
    Returns:
        Human-readable explanation
    """
    err_msg = str(err)
    return Explanation(
        title="Module cannot be imported",
        reason="You tried to import a module that doesn't exist, isn't installed, "
                "or has an error preventing it from loading.",
        suggestions=[
            "Verify the module name is spelled correctly (case-sensitive for Unix)",
            "Check if the module is installed: pip list | grep module_name",
            "Install the module: pip install module_name",
            "Check for circular imports or syntax errors in the module",
            "For relative imports, ensure __init__.py files exist in package directories",
            f"Error details: {err_msg}"
        ],
        context="Use pip install to add missing modules"
    )


# Registry of explainers
EXPLAINERS: Dict[Type[Exception], Callable[[Exception], Explanation]] = {
    KeyError: explain_key_error,
    IndexError: explain_index_error,
    TypeError: explain_type_error,
    ValueError: explain_value_error,
    AttributeError: explain_attribute_error,
    NameError: explain_name_error,
    ZeroDivisionError: explain_zero_division_error,
    FileNotFoundError: explain_file_not_found_error,
    ImportError: explain_import_error,
}


def register_explainer(exception_type: Type[Exception], explainer: Callable[[Exception], Explanation]) -> None:
    """
    Register a custom explainer for an exception type.
    
    Args:
        exception_type: The exception class to handle
        explainer: A callable that takes an exception and returns an Explanation
    
    Example:
        def my_custom_explainer(err):
            return Explanation(
                title="My custom error",
                reason="This is why it happened",
                suggestions=["Fix it this way", "Or this way"]
            )
        
        register_explainer(MyException, my_custom_explainer)
    """
    EXPLAINERS[exception_type] = explainer


def get_explainer(exception_type: Type[Exception]) -> Optional[Callable[[Exception], Explanation]]:
    """
    Get the explainer for an exception type, with subclass fallback.
    
    This first tries an exact match, then walks the MRO (method resolution order)
    to find the nearest registered base exception class.
    
    Args:
        exception_type: The exception class
    
    Returns:
        The explainer function, or None if not registered
    """
    # Exact match
    explainer = EXPLAINERS.get(exception_type)
    if explainer:
        return explainer
    
    # Subclass fallback: walk MRO to find a registered base class
    for base in getattr(exception_type, "__mro__", [])[1:]:  # skip the class itself
        explainer = EXPLAINERS.get(base)
        if explainer:
            return explainer
    
    return None
