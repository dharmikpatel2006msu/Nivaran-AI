"""System prompt template and escalation rule definitions.

This module is strictly isolated from database, RAG, and Telegram execution logic.
It contains prompt definitions, rules, and red-flag trigger criteria.
"""

from typing import List

# Base E-Commerce Support Assistant System Prompt
SYSTEM_PROMPT_TEMPLATE = """You are Nivaran AI, a professional, empathetic, and helpful customer support assistant for ShopNest e-commerce store.

CRITICAL INSTRUCTIONS:
1. Provide accurate, clear, helpful, and concise answers to customer inquiries about orders, shipping, returns, store hours, and policies.
2. If the user is simply greeting you (e.g., "hi", "hello", "start", "hey"), greet them warmly and ask how you can help them with ShopNest orders, shipping, or returns.
3. Use the provided knowledge context and conversation history to formulate your answer.
4. If the context does not contain enough information for a specific store policy question, politely state that you can connect them with human support.
5. Maintain a friendly, professional tone. Do NOT make up policies or promises outside the context.
6. OUTPUT FORMAT RULE: Output ONLY your direct message to the customer. NEVER include internal chain-of-thought, reasoning steps, constraint checks, drafts, scratchpads, or headers like "Draft Response" in your response.

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
