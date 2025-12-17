"""
Basic usage examples demonstrating whyfail features.
"""
import whyfail

print("Example: KeyError")
with whyfail.explain(reraise=False):
    data = {"name": "Alice"}
    print(data["user_id"])  # KeyError

print("\nExample: IndexError")
with whyfail.explain(reraise=False):
    items = [1, 2, 3]
    print(items[10])

print("\nExample: TypeError")
with whyfail.explain(reraise=False):
    print("hello" + 5)

print("\nExample: ValueError")
with whyfail.explain(reraise=False):
    print(int("not a number"))

print("\nExample: AttributeError")
with whyfail.explain(reraise=False):
    obj = "string"
    obj.nonexistent_method()

print("\nExample: ZeroDivisionError")
with whyfail.explain(reraise=False):
    print(10 / 0)

print("\nExample: FileNotFoundError")
with whyfail.explain(reraise=False):
    with open("/nonexistent/file.txt") as f:
        pass

print("\nExample: ImportError")
with whyfail.explain(reraise=False):
    import nonexistent_module_xyz
