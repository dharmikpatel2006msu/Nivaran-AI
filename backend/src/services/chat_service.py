"""Chat Service Orchestrator for Nivaran AI.

Coordinates user resolution, conversational memory window retrieval, RAG retrieval,
LLM completion, message logging, and in-house escalation ticketing.
"""

import logging
from datetime import datetime
from typing import Tuple, List, Dict, Any
from src.config import CHAT_HISTORY_WINDOW, SIMILARITY_THRESHOLD
from src.db.supabase_client import get_supabase_client
from src.rag.retriever import retrieve_context
from src.rag.generator import generate_llm_response
from src.services.escalation_service import evaluate_escalation_triggers, create_in_house_ticket

logger = logging.getLogger(__name__)


def get_or_create_user(telegram_id: int, name: str) -> Dict[str, Any]:
    """Ensures user exists in the `users` table and updates `last_active_at`.

    Args:
        telegram_id: Telegram user ID.
        name: Display name or handle.

    Returns:
        User record dictionary.
    """
    supabase = get_supabase_client()
    now_iso = datetime.utcnow().isoformat()

    try:
        # Check existing user
        response = supabase.table("users").select("*").eq("telegram_id", telegram_id).execute()
        if response.data and len(response.data) > 0:
            user = response.data[0]
            # Update last_active_at timestamp
            supabase.table("users").update({"last_active_at": now_iso, "name": name}).eq("id", user["id"]).execute()
            return user

        # Create new user
        new_user_data = {
            "telegram_id": telegram_id,
            "name": name,
            "created_at": now_iso,
            "last_active_at": now_iso
        }
        create_res = supabase.table("users").insert(new_user_data).execute()
        return create_res.data[0]
    except Exception as e:
        logger.error(f"Error upserting user telegram_id={telegram_id}: {e}")
        return {"id": 0, "telegram_id": telegram_id, "name": name}


def fetch_recent_history(user_id: int, limit: int = CHAT_HISTORY_WINDOW) -> List[Dict[str, Any]]:
    """Pulls the last N messages for a user to construct short-term context.

    Uses `CHAT_HISTORY_WINDOW` (default 5).
    """
    if user_id <= 0:
        return []

    try:
        supabase = get_supabase_client()
        response = (
            supabase.table("chat_history")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        # Reverse to return in chronological order (oldest to newest)
        history = response.data or []
        return list(reversed(history))
    except Exception as e:
        logger.error(f"Error fetching chat history for user_id={user_id}: {e}")
        return []


def log_chat_message(user_id: int, role: str, content: str) -> None:
    """Logs a single message ('user' or 'assistant') to the `chat_history` table."""
    if user_id <= 0:
        return

    try:
        supabase = get_supabase_client()
        supabase.table("chat_history").insert({
            "user_id": user_id,
            "role": role,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        }).execute()
    except Exception as e:
        logger.error(f"Error logging chat message role={role} user_id={user_id}: {e}")


def format_history_for_prompt(history: List[Dict[str, Any]]) -> str:
    """Formats a list of history records into a prompt string."""
    formatted_lines = []
    for msg in history:
        role = "User" if msg.get("role") == "user" else "Assistant"
        formatted_lines.append(f"{role}: {msg.get('content', '')}")
    return "\n".join(formatted_lines)


def count_unresolved_turns(history: List[Dict[str, Any]]) -> int:
    """Calculates consecutive unresolved or low-confidence turns from recent history."""
    unresolved_indicators = [
        "escalat", "human support", "apologize", "unable to find",
        "don't have information", "not enough information", "representative", "ticket #"
    ]
    count = 0
    # Traverse from most recent messages backwards
    for msg in reversed(history):
        if msg.get("role") == "assistant":
            content = msg.get("content", "").lower()
            if any(ind in content for ind in unresolved_indicators):
                count += 1
            else:
                break
    return count


def process_incoming_message(telegram_id: int, user_display_name: str, message_text: str) -> str:
    """End-to-end orchestration pipeline for an incoming user message.

    Workflow:
    1. Upsert user record in `users` table.
    2. Fetch last `CHAT_HISTORY_WINDOW` messages for conversational context.
    3. Generate embedding & query pgvector for matching knowledge chunks.
    4. Generate candidate reply using Groq LLM with context & history.
    5. Evaluate escalation triggers (red flags, low confidence, chunk tags, unresolved count).
    6. Log user message and assistant reply to `chat_history`.
    7. If escalated, create a row in `tickets` table and append human support notice.

    Returns:
        Final reply text to be sent back to Telegram user.
    """
    logger.info(f"📩 Processing message from user '{user_display_name}' ({telegram_id}): '{message_text[:50]}...'")

    # Step 1: User resolution
    user = get_or_create_user(telegram_id, user_display_name)
    user_id = user.get("id", 0)

    # Step 2: Fetch short-term history window (last CHAT_HISTORY_WINDOW messages)
    history_records = fetch_recent_history(user_id, limit=CHAT_HISTORY_WINDOW)
    formatted_history = format_history_for_prompt(history_records)
    recent_unresolved = count_unresolved_turns(history_records)

    # Log incoming user message
    log_chat_message(user_id, "user", message_text)

    # Step 3: RAG Retrieval
    docs, max_similarity = retrieve_context(message_text, match_threshold=SIMILARITY_THRESHOLD, match_count=3)

    # Step 4: LLM Reply Generation
    ai_reply = generate_llm_response(message_text, docs, formatted_history)

    # Step 5: Escalation Evaluation
    should_escalate, escalation_reason = evaluate_escalation_triggers(
        user_message=message_text,
        max_similarity=max_similarity,
        context_documents=docs,
        recent_unresolved_count=recent_unresolved
    )

    final_reply = ai_reply

    # Step 6: Handle Escalation Action
    if should_escalate:
        logger.info(f"⚠️ Message triggered escalation. Reason: {escalation_reason}")
        created_ticket = create_in_house_ticket(user_id, escalation_reason)

        ticket_id = created_ticket.get("id") if created_ticket else "N/A"
        escalation_notice = (
            f"\n\n--- Support Ticket #{ticket_id} Created ---\n"
            "Your request has been logged with our customer support team. "
            "A representative will review your issue shortly."
        )
        final_reply += escalation_notice

    # Log assistant response
    log_chat_message(user_id, "assistant", final_reply)

    return final_reply
