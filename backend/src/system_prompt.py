"""System prompt template and escalation rule definitions.

This module is strictly isolated from database, RAG, and Telegram execution logic.
It contains prompt definitions, rules, and red-flag trigger criteria.
"""

from typing import List

# Base E-Commerce Support Assistant System Prompt
SYSTEM_PROMPT_TEMPLATE = """You are Nivaran AI, a professional, empathetic, and helpful customer support assistant for our e-commerce store.

Your Objectives:
1. Provide accurate, clear, and concise answers to customer inquiries about orders, shipping, returns, store hours, and policies.
2. Use ONLY the provided knowledge context and recent conversation history to formulate your answer.
3. If the context does not contain enough information to resolve the user's issue, politely state that you are escalating the matter to our human support team.
4. Maintain a polite, professional, and brand-friendly tone at all times. Do NOT invent policies or make promises outside the context.

--- RECENT CONVERSATION HISTORY ---
{chat_history}

--- KNOWLEDGE BASE CONTEXT ---
{knowledge_context}
"""

# Red-flag keywords that trigger mandatory human escalation
# TODO: Team input needed — review and expand red-flag keyword triggers for e-commerce vertical
RED_FLAG_KEYWORDS: List[str] = [
    "damaged",
    "defective",
    "broken",
    "fraud",
    "scam",
    "stolen card",
    "unauthorized charge",
    "lawsuit",
    "legal action",
    "chargeback",
    "never received",
    "stolen package",
]

# TODO: Team input needed — define sentiment analysis or repetition thresholds for escalation
MAX_UNRESOLVED_CONVERSATION_TURNS = 3


def build_system_prompt(knowledge_context: str, chat_history_formatted: str) -> str:
    """Formats the system prompt with retrieved knowledge context and recent chat history.

    Args:
        knowledge_context: Concatenated text chunks retrieved from Supabase pgvector.
        chat_history_formatted: Formatted string of recent user/assistant messages.

    Returns:
        Fully assembled system prompt ready for LLM invocation.
    """
    if not knowledge_context.strip():
        knowledge_context = "No direct matching knowledge base articles found."

    if not chat_history_formatted.strip():
        chat_history_formatted = "No prior messages in this conversation session."

    return SYSTEM_PROMPT_TEMPLATE.format(
        knowledge_context=knowledge_context,
        chat_history=chat_history_formatted
    )
