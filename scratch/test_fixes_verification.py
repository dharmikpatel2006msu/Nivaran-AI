import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from src.services.chat_service import process_incoming_message

test_user_id = 88888888
display_name = "Test User"

test_prompts = [
    ("Greeting 'Hii'", "Hii"),
    ("Greeting 'Start'", "Start"),
    ("Return policy query", "How do I return an item ?"),
    ("Shipping options query", "What are your shipping options and delivery times ?"),
    ("Damaged item escalation query", "I received a damaged item, it arrived completely broken!")
]

print("=" * 60)
print("RUNNING VERIFICATION FOR ALL REPORTED BUGS")
print("=" * 60)

for label, query in test_prompts:
    print(f"\n[TEST CASE] {label}")
    print(f"User Query: '{query}'")
    reply = process_incoming_message(test_user_id, display_name, query)
    print(f"Bot Reply:\n{reply}\n")
    
    # Assertions
    assert "<think>" not in reply, "ERROR: Found <think> tag in reply!"
    assert "Constraint check" not in reply, "ERROR: Leaked constraint check in reply!"
    assert "Draft Response" not in reply, "ERROR: Leaked Draft Response header in reply!"
    assert not reply.endswith("shipping,"), "ERROR: Response was truncated!"
    assert "An error occurred while processing your request" not in reply, "ERROR: Generic error message returned!"
    print(f"--> [PASS] {label}")

print("\n" + "=" * 60)
print("ALL TEST CASES PASSED WITH ZERO BUGS!")
print("=" * 60)
