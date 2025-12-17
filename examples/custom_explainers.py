"""
Example demonstrating custom explainer registration.
"""
import whyfail
from whyfail import Explanation

class CustomError(Exception):
    pass

def explain_custom_error(err: CustomError) -> Explanation:
    return Explanation(
        title="Custom error occurred",
        reason="A custom condition triggered this error",
        suggestions=[
            "Check your custom logic",
            "Add validation for inputs",
            "Provide a safe fallback"
        ],
        context=str(err)
    )

whyfail.register_explainer(CustomError, explain_custom_error)

print("Example: CustomError")
with whyfail.explain(reraise=False):
    raise CustomError("oops")
