"""
Example demonstrating teaching/educational configuration.
"""
import whyfail

# Configure whyfail for teaching mode (no traceback, no re-raise)
whyfail.configure(show_traceback=False, reraise=False)

print("Teaching Mode: Demonstrating common mistakes")

with whyfail.explain():
    # NameError
    print(undefined_variable)

with whyfail.explain():
    # IndexError
    values = [1, 2, 3]
    print(values[100])
