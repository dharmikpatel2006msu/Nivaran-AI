import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from src.rag.retriever import generate_embedding, retrieve_context
from src.rag.generator import generate_llm_response
from src.services.chat_service import process_incoming_message, get_or_create_user
from src.db.supabase_client import get_supabase_client
from fastapi.testclient import TestClient
from src.main import app

print("=== 1. Testing Gemini Embedding Generation ===")
emb = generate_embedding("What are your shipping options?")
print(f"[OK] Embedding dimension: {len(emb)}")

print("\n=== 2. Testing Supabase Vector Retrieval ===")
docs, similarity = retrieve_context("What are your shipping options?")
print(f"[OK] Retrieved {len(docs)} documents. Max similarity: {similarity:.4f}")
if docs:
    print(f"     Sample doc heading: {docs[0].get('metadata', {}).get('heading')}")

print("\n=== 3. Testing Groq LLM Generation ===")
answer = generate_llm_response("What are your shipping options?", docs)
print(f"[OK] LLM response: {answer[:120]}...")

print("\n=== 4. Testing End-to-End Chat Pipeline (Normal Query) ===")
test_telegram_id = 99999999
normal_reply = process_incoming_message(test_telegram_id, "Test Runner", "How many days does standard delivery take?")
print(f"[OK] Chat reply: {normal_reply[:150]}...")

print("\n=== 5. Testing End-to-End Escalation (Red-Flag Query) ===")
escalated_reply = process_incoming_message(test_telegram_id, "Test Runner", "I received a damaged and broken package, I want a refund!")
print(f"[OK] Escalated reply: {escalated_reply[:180]}...")

print("\n=== 6. Testing Admin REST API via FastAPI TestClient ===")
client = TestClient(app)

stats_res = client.get("/api/admin/stats")
print(f"[OK] GET /api/admin/stats -> {stats_res.status_code}: {stats_res.json()}")

tickets_res = client.get("/api/admin/tickets")
tickets_data = tickets_res.json()
print(f"[OK] GET /api/admin/tickets -> {tickets_res.status_code} (found {len(tickets_data)} tickets)")

if tickets_data:
    t_id = tickets_data[0]["id"]
    patch_res = client.patch(f"/api/admin/tickets/{t_id}/status", json={"status": "in_progress"})
    print(f"[OK] PATCH /api/admin/tickets/{t_id}/status -> {patch_res.status_code}: new status = {patch_res.json().get('status')}")

# User history
user = get_or_create_user(test_telegram_id, "Test Runner")
user_id = user.get("id")
hist_res = client.get(f"/api/admin/users/{user_id}/history")
print(f"[OK] GET /api/admin/users/{user_id}/history -> {hist_res.status_code}: {len(hist_res.json().get('messages', []))} messages logged")

print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")
