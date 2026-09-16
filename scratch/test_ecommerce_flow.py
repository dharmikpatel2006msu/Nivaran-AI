"""End-to-end verification script for E-Commerce Storefront & Telegram Deep-Linking Order Tracking."""

import os
import sys

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from src.rag.retriever import get_user_active_orders
from src.system_prompt import build_system_prompt
from src.rag.generator import clean_llm_output
from src.services.chat_service import process_incoming_message, get_or_create_user

def test_system_prompt_injection():
    print("=== Test 1: Active Order Prompt Formatting ===")
    mock_orders_formatted = "- Order #ORD-88219: Wireless Headphones ($99.99) | Status: processing"
    prompt = build_system_prompt(
        knowledge_context="Standard delivery takes 3-5 business days.",
        chat_history_formatted="User: Where is my order?",
        active_orders_formatted=mock_orders_formatted
    )
    assert "--- ACTIVE CUSTOMER ORDERS ---" in prompt
    assert "ORD-88219" in prompt
    print("✅ System prompt includes ACTIVE CUSTOMER ORDERS successfully!")

def test_pipeline_import_and_execution():
    print("\n=== Test 2: Pipeline Integration Test ===")
    user_id = 999888777
    user_name = "Test Buyer"
    user = get_or_create_user(user_id, user_name)
    print(f"✅ User resolved: {user}")

    # Process query where user asks about order status
    reply = process_incoming_message(user_id, user_name, "Where is my order status?")
    print(f"🤖 AI Reply snippet: {reply[:150]}...")
    print("✅ Pipeline executed successfully!")

if __name__ == "__main__":
    test_system_prompt_injection()
    test_pipeline_import_and_execution()
    print("\n🎉 ALL E-COMMERCE VERIFICATION TESTS PASSED SUCCESSFULLY!")
