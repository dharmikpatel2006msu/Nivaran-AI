"""In-house Escalation Service for Nivaran AI.

Replaces external Trello integration (previously `createTrelloTicket` in `index.js` lines 25-46).
Evaluates red-flag criteria, low retrieval confidence, and metadata escalation tags,
and writes an escalation record directly to the Supabase `tickets` table (`status`: 'open').
"""

import logging
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime
from src.system_prompt import RED_FLAG_KEYWORDS
from src.config import SIMILARITY_THRESHOLD, LOW_CONFIDENCE_THRESHOLD, REPEATED_UNRESOLVED_THRESHOLD
from src.db.supabase_client import get_supabase_client
from src.db.models import TicketStatus

logger = logging.getLogger(__name__)


GREETINGS_LIST = {
    "hi", "hii", "hiii", "hello", "hey", "heyy", "start", "/start",
    "help", "good morning", "good afternoon", "good evening", "namaste", "hola", "howdy"
}


def is_simple_greeting(message: str) -> bool:
    """Checks if a user message is a simple greeting or conversation opener."""
    cleaned = "".join(c for c in message.lower() if c.isalnum() or c.isspace()).strip()
    words = cleaned.split()
    if cleaned in GREETINGS_LIST:
        return True
    if len(words) <= 2 and any(w in GREETINGS_LIST for w in words):
        return True
    return False


def evaluate_escalation_triggers(
    user_message: str,
    max_similarity: float,
    context_documents: List[Dict[str, Any]],
    recent_unresolved_count: int = 0
) -> Tuple[bool, str]:
    """Evaluates whether a message or state warrants human escalation.

    Triggers:
    1. Knowledge chunk metadata tagged `escalate: True`.
    2. Red-flag keyword matches in user query.
    3. Low similarity confidence score (below threshold, excluding greetings).
    4. Repeated unresolved queries.

    Returns:
        Tuple of (should_escalate: bool, escalation_reason: str).
    """
    user_msg_lower = user_message.lower()

    # 1. Metadata Tag Check (`escalate: true` on retrieved knowledge chunk)
    for doc in context_documents:
        metadata = doc.get("metadata") or {}
        if metadata.get("escalate") in [True, "true", "True", 1]:
            reason = f"Knowledge base chunk tagged for mandatory escalation (Category: {metadata.get('category', 'unknown')})"
            logger.info(f"🚩 Escalation triggered: {reason}")
            return True, reason

    # 2. Red-Flag Keyword Trigger
    for keyword in RED_FLAG_KEYWORDS:
        if keyword in user_msg_lower:
            reason = f"Red-flag phrase detected in user query: '{keyword}'"
            logger.info(f"🚩 Escalation triggered: {reason}")
            return True, reason

    # 3. Low Confidence / Knowledge Gap Trigger (Skipped for greetings)
    if not is_simple_greeting(user_message):
        if max_similarity < LOW_CONFIDENCE_THRESHOLD:
            reason = f"Low knowledge retrieval confidence score ({max_similarity:.4f} < {LOW_CONFIDENCE_THRESHOLD})"
            logger.info(f"🚩 Escalation triggered: {reason}")
            return True, reason

    # 4. Repeated Unresolved Query Trigger
    if recent_unresolved_count >= REPEATED_UNRESOLVED_THRESHOLD:
        reason = f"User reached repeated unresolved query threshold ({recent_unresolved_count} turns)"
        logger.info(f"🚩 Escalation triggered: {reason}")
        return True, reason

    return False, ""


def create_in_house_ticket(
    user_id: int,
    escalation_reason: str,
    order_id: Optional[str] = None,
    issue_description: Optional[str] = None,
    issue: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Inserts a new ticket into the Supabase `tickets` table with multi-tier schema fallback.

    Args:
        user_id: Foreign key ID of the user.
        escalation_reason: Explanation of why the ticket was opened.
        order_id: Linked order ID if available (e.g. 'ORD-69Z2N').
        issue_description: Detailed customer message content.
        issue: Customer issue text.

    Returns:
        Inserted ticket record dict or None on failure.
    """
    logger.info(f"📋 Creating in-house support ticket for user_id={user_id} (Order: {order_id})...")
    supabase = get_supabase_client()
    now_iso = datetime.utcnow().isoformat()

    issue_content = issue or issue_description

    # Attempt 1: Full payload with order_id, issue, and issue_description
    ticket_data_full = {
        "user_id": user_id,
        "status": TicketStatus.OPEN.value,
        "escalation_reason": escalation_reason,
        "order_id": order_id,
        "issue": issue_content,
        "issue_description": issue_content,
        "created_at": now_iso
    }
    try:
        response = supabase.table("tickets").insert(ticket_data_full).execute()
        if response.data and len(response.data) > 0:
            created_ticket = response.data[0]
            logger.info(f"✅ Created ticket ID {created_ticket.get('id')} with status 'open'.")
            return created_ticket
    except Exception as e:
        logger.warning(f"⚠️ Primary ticket insert failed ({e}), attempting fallback without order_id FK...")

    # Attempt 2: Fallback without order_id (in case FK constraint fails or order_id missing)
    ticket_data_no_order = {
        "user_id": user_id,
        "status": TicketStatus.OPEN.value,
        "escalation_reason": escalation_reason,
        "issue_description": issue_description,
        "created_at": now_iso
    }
    try:
        response = supabase.table("tickets").insert(ticket_data_no_order).execute()
        if response.data and len(response.data) > 0:
            created_ticket = response.data[0]
            logger.info(f"✅ Created ticket ID {created_ticket.get('id')} via fallback 1.")
            return created_ticket
    except Exception as e:
        logger.warning(f"⚠️ Fallback 1 ticket insert failed ({e}), attempting minimal schema insert...")

    # Attempt 3: Minimal insert matching baseline migration 02 schema (user_id, status, escalation_reason)
    ticket_data_minimal = {
        "user_id": user_id,
        "status": TicketStatus.OPEN.value,
        "escalation_reason": escalation_reason,
        "created_at": now_iso
    }
    try:
        response = supabase.table("tickets").insert(ticket_data_minimal).execute()
        if response.data and len(response.data) > 0:
            created_ticket = response.data[0]
            logger.info(f"✅ Created ticket ID {created_ticket.get('id')} via minimal fallback.")
            return created_ticket
    except Exception as e:
        logger.error(f"❌ All ticket creation attempts failed in Supabase: {e}")

    return None
