"""System prompt template and escalation rule definitions.

This module is strictly isolated from database, RAG, and Telegram execution logic.
It contains prompt definitions, rules, and red-flag trigger criteria.
"""

from typing import List

# Base E-Commerce Support Assistant System Prompt
SYSTEM_PROMPT_TEMPLATE = """You are Nivaran AI, a professional, empathetic, and helpful customer support assistant for ShopNest e-commerce store.

CRITICAL INSTRUCTIONS:
1. Provide accurate, clear, helpful, and concise answers to customer inquiries about orders, shipping, returns, store hours, and policies.
2. If the user is asking about their order status or tracking, reference their active orders listed below if available.
3. If the user is simply greeting you (e.g., "hi", "hello", "start", "hey"), greet them warmly and ask how you can help them with ShopNest orders, shipping, or returns.
4. Use the provided active customer orders, knowledge context, and conversation history to formulate your answer.
5. If an issue requires human support or returns team intervention (e.g., damaged or missing items), reassure the customer empathetically.
6. Do NOT invent non-existent UI navigation steps (such as "My Orders -> Order Details -> Return Item"). Reassure the user that support staff will contact them directly with return instructions.
7. Maintain a friendly, professional tone. Do NOT make up policies or promises outside the context.
8. CRITICAL TICKET RULE: Do NOT invent, fabricate, or guess ticket numbers (e.g., "Ticket #11") or tell the user you created a ticket number yourself. The backend automated system automatically creates and attaches official support ticket records.
9. OUTPUT FORMAT RULE: Output ONLY your direct message to the customer. NEVER include internal chain-of-thought, reasoning steps, constraint checks, drafts, scratchpads, or headers like "Draft Response" in your response.

--- ACTIVE CUSTOMER ORDERS ---
{active_orders}

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


def build_system_prompt(
    knowledge_context: str,
    chat_history_formatted: str,
    active_orders_formatted: str = ""
) -> str:
    """Formats the system prompt with active customer orders, retrieved knowledge context, and chat history.

    Args:
        knowledge_context: Concatenated text chunks retrieved from Supabase pgvector.
        chat_history_formatted: Formatted string of recent user/assistant messages.
        active_orders_formatted: Formatted list of user's linked active orders.

    Returns:
        Fully assembled system prompt ready for LLM invocation.
    """
    if not knowledge_context.strip():
        knowledge_context = "No direct matching knowledge base articles found."

    if not chat_history_formatted.strip():
        chat_history_formatted = "No prior messages in this conversation session."

    if not active_orders_formatted.strip():
        active_orders_formatted = "No linked active orders found for this customer account."

    return SYSTEM_PROMPT_TEMPLATE.format(
        knowledge_context=knowledge_context,
        chat_history=chat_history_formatted,
        active_orders=active_orders_formatted
    )
