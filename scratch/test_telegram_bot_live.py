import sys
import os
import asyncio
from dotenv import load_dotenv

backend_dir = os.path.join(os.path.dirname(__file__), "..", "backend")
sys.path.insert(0, backend_dir)
load_dotenv(os.path.join(backend_dir, ".env"))

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from telegram import Bot
from src.config import TELEGRAM_BOT_TOKEN, TELEGRAM_MODE, WEBHOOK_URL
from src.rag.retriever import generate_embedding, retrieve_context
from src.rag.generator import generate_llm_response
from src.services.chat_service import process_incoming_message, get_or_create_user

async def verify_telegram():
    print("==================================================")
    print("   NIVARAN AI — TELEGRAM BOT DIAGNOSTIC & TEST    ")
    print("==================================================")
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN is not set in backend/.env")
        return
        
    print(f"🔹 Configured Telegram Mode: {TELEGRAM_MODE}")
    
    # 1. Telegram API Verification
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    try:
        me = await bot.get_me()
        print(f"✅ Telegram Bot Connected Successfully!")
        print(f"   • Bot ID: {me.id}")
        print(f"   • Bot Name: {me.first_name}")
        print(f"   • Username: @{me.username}")
        print(f"   • Direct Link: https://t.me/{me.username}")
        
        # Check webhook status
        webhook_info = await bot.get_webhook_info()
        print(f"   • Current Webhook URL: '{webhook_info.url or 'None (Polling Mode)'}'")
        print(f"   • Pending Update Count: {webhook_info.pending_update_count}")
        
    except Exception as e:
        print(f"❌ Failed to connect to Telegram Bot API: {e}")
        return

    # 2. Embedding & Vector Retrieval Verification
    print("\n--------------------------------------------------")
    print("🔹 Testing Vector DB & RAG Knowledge Retrieval...")
    test_query = "What is your refund and return policy?"
    try:
        docs, similarity = retrieve_context(test_query)
        print(f"✅ RAG Context Retrieved ({len(docs)} chunks matched, max similarity: {similarity:.2f})")
        for i, d in enumerate(docs, 1):
            heading = d.get('metadata', {}).get('heading', 'Untitled')
            print(f"   [{i}] Heading: '{heading}' | Snippet: {d.get('content', '')[:70]}...")
    except Exception as e:
        print(f"❌ RAG Retrieval Error: {e}")

    # 3. End-to-End Chat & Escalation Simulation
    print("\n--------------------------------------------------")
    print("🔹 Testing Simulated Telegram User Interaction...")
    test_tg_id = 12345678
    test_user_name = "Telegram Test User"
    
    # Normal Query
    print(f"\n[Test 1: General Inquiry] Query: '{test_query}'")
    reply = process_incoming_message(test_tg_id, test_user_name, test_query)
    print(f"🤖 Bot Response:\n{reply}\n")
    
    # Red-flag Escalation Query
    redflag_query = "My item arrived damaged and broken, I want to talk to a manager immediately!"
    print(f"[Test 2: Red-Flag Escalation] Query: '{redflag_query}'")
    reply_esc = process_incoming_message(test_tg_id, test_user_name, redflag_query)
    print(f"🤖 Bot Response (Escalated):\n{reply_esc}\n")

    print("==================================================")
    print(f"🚀 Telegram Bot is READY!")
    print(f"👉 To chat with the bot live, open: https://t.me/{me.username}")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(verify_telegram())
