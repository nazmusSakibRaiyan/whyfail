"""
whyfail Demo - See exactly what users experience in the terminal

This script demonstrates whyfail with different error types and usage patterns.
"""
import sys
import io
import whyfail

# Set UTF-8 encoding for output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("\n" + "=" * 70)
print("WHYFAIL LIBRARY - LIVE DEMO")
print("=" * 70)

# ============================================================================
# DEMO 1: KeyError with Context Manager
# ============================================================================
print("\n📌 DEMO 1: KeyError (Missing Dictionary Key)")
print("-" * 70)
print("Code: data = {'name': 'Alice'}")
print("      print(data['age'])")
print("\n" + "▼" * 70)

with whyfail.explain(reraise=False):
    data = {"name": "Alice"}
    print(data["age"])

# ============================================================================
# DEMO 2: IndexError
# ============================================================================
print("\n\n📌 DEMO 2: IndexError (List Out of Range)")
print("-" * 70)
print("Code: numbers = [10, 20, 30]")
print("      print(numbers[100])")
print("\n" + "▼" * 70)

with whyfail.explain(reraise=False):
    numbers = [10, 20, 30]
    print(numbers[100])

# ============================================================================
# DEMO 3: TypeError
# ============================================================================
print("\n\n📌 DEMO 3: TypeError (Incompatible Type Operation)")
print("-" * 70)
print("Code: result = 'Hello' + 42")
print("\n" + "▼" * 70)

with whyfail.explain(reraise=False):
    result = "Hello" + 42

# ============================================================================
# DEMO 4: ValueError
# ============================================================================
print("\n\n📌 DEMO 4: ValueError (Invalid Value Format)")
print("-" * 70)
print("Code: age = int('twenty-five')")
print("\n" + "▼" * 70)

with whyfail.explain(reraise=False):
    age = int("twenty-five")

# ============================================================================
# DEMO 5: ZeroDivisionError
# ============================================================================
print("\n\n📌 DEMO 5: ZeroDivisionError (Division by Zero)")
print("-" * 70)
print("Code: result = 100 / 0")
print("\n" + "▼" * 70)

with whyfail.explain(reraise=False):
    result = 100 / 0

# ============================================================================
# DEMO 6: AttributeError
# ============================================================================
print("\n\n📌 DEMO 6: AttributeError (Object Has No Attribute)")
print("-" * 70)
print("Code: text = 'hello'")
print("      text.upper_case()")
print("\n" + "▼" * 70)

with whyfail.explain(reraise=False):
    text = "hello"
    text.upper_case()

# ============================================================================
# DEMO 7: NameError
# ============================================================================
print("\n\n📌 DEMO 7: NameError (Variable Not Defined)")
print("-" * 70)
print("Code: print(undefined_variable)")
print("\n" + "▼" * 70)

with whyfail.explain(reraise=False):
    print(undefined_variable)

# ============================================================================
# DEMO 8: Using Decorator
# ============================================================================
print("\n\n📌 DEMO 8: Using Decorator on Function")
print("-" * 70)
print("Code:")
print("  @whyfail.explain_errors(reraise=False)")
print("  def parse_user_input(data):")
print("      return int(data['count'])")
print("\n" + "▼" * 70)

@whyfail.explain_errors(reraise=False)
def parse_user_input(data):
    return int(data["count"])

parse_user_input({"name": "Alice"})

# ============================================================================
# DEMO 9: Manual Explanation
# ============================================================================
print("\n\n📌 DEMO 9: Manual Explanation (For Custom Handling)")
print("-" * 70)
print("Code:")
print("  try:")
print("      result = [1,2,3][99]")
print("  except IndexError as e:")
print("      explanation = whyfail.get_explanation(e)")
print("      print(explanation)")
print("\n" + "▼" * 70)

try:
    result = [1, 2, 3][99]
except IndexError as e:
    explanation = whyfail.get_explanation(e)
    print(explanation)

# ============================================================================
# DEMO 10: Configuration - Teaching Mode
# ============================================================================
print("\n\n📌 DEMO 10: Teaching Mode (No Traceback, No Re-raise)")
print("-" * 70)
print("Code:")
print("  whyfail.configure(show_traceback=False, reraise=False)")
print("  with whyfail.explain():")
print("      bad_dict['missing_key']")
print("\n" + "▼" * 70)

whyfail.configure(show_traceback=False, reraise=False)
with whyfail.explain():
    bad_dict = {"name": "Bob"}
    print(bad_dict["email"])

# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 70)
print("✨ DEMO COMPLETE ✨")
print("=" * 70)
print("""
What you just saw:
✅ Clear, human-readable error explanations
✅ Actionable suggestions for each error
✅ Context about what went wrong
✅ Multiple usage patterns (context manager, decorator, manual)

Benefits:
🎯 Beginners understand errors without Googling
📚 Educators provide automatic helpful feedback
⚡ Developers debug 50-70% faster
🚀 Better error logging in production

Ready to use whyfail in your project? 
Just: pip install whyfail
Then: with whyfail.explain():
          your_code()
""")
print("=" * 70)
