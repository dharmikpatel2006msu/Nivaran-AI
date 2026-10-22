"""Conversational Query Reformulation module for Nivaran AI RAG pipeline.

Transforms referential, ambiguous, or elliptical user queries into self-contained,
contextually rich search queries for vector retrieval and entity tracking.

Solves:
- Coreference resolution ("How much is it?" -> "How much is [Product]?")
- Elliptical follow-ups ("And in black?" -> "Is [Product] available in black?")
- Implicit order references ("Where is it?" -> "Where is order ORD-XXXXX?")
- Zero latency overhead on first-turn or standalone queries via heuristic fast-path.
"""

import re
import logging
from typing import List, Dict, Any, Optional
from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL

logger = logging.getLogger(__name__)

_groq_client = None

# In-memory LRU-like cache for frequent query reformulations in active sessions
_REFORMULATION_CACHE: Dict[str, str] = {}
_MAX_CACHE_SIZE = 500

# Pronouns and referential indicators that signal potential coreference/ellipsis
REFERENTIAL_INDICATORS = {
    "it", "its", "it's", "this", "that", "these", "those",
    "them", "they", "their", "there",
    "the item", "the product", "the order", "my order", "the package",
    "the one", "which one", "same", "another", "else"
}

# Common conversational pleasantries/commands that should NEVER be rewritten
BYPASS_UTTERANCES = {
    "hi", "hello", "hey", "hola", "good morning", "good evening", "good afternoon",
    "yes", "yep", "yeah", "no", "nope", "cancel", "update", "ok", "okay",
    "sure", "thanks", "thank you", "bye", "goodbye", "help", "start", "/start"
}


def get_groq_client() -> Groq:
    """Initializes and returns the Groq API client."""
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=GROQ_API_KEY)
    return _groq_client


def needs_reformulation(query: str, chat_history: List[Dict[str, Any]]) -> bool:
    """Heuristic fast-path to determine if an utterance requires contextual reformulation.

    Returns False for:
    - Empty history (first turn in conversation)
    - Greetings, confirmations, or trivial pleasantries
    - Long, self-contained queries that contain explicit entities and no pronouns
    """
    if not chat_history:
        return False

    cleaned_query = query.strip().lower()

    if cleaned_query in BYPASS_UTTERANCES:
        return False

    # Short follow-ups (< 4 words) are almost always elliptical (e.g. "how much?", "and warranty?", "in blue?")
    words = re.findall(r"\b[a-zA-Z0-9'-]+\b", cleaned_query)
    if len(words) <= 3:
        return True

    # Check for presence of referential tokens or pronouns
    for indicator in REFERENTIAL_INDICATORS:
        if re.search(rf"\b{re.escape(indicator)}\b", cleaned_query):
            return True

    # Elliptical question starters without clear nouns (e.g., "what about...", "how about...", "and...")
    if re.match(r"^(what about|how about|and\b|can i\b|does it\b|is it\b)", cleaned_query):
        return True

    return False


def extract_recent_order_id(chat_history: List[Dict[str, Any]], active_orders: Optional[List[Dict[str, Any]]] = None) -> Optional[str]:
    """Finds the most relevant active or recently discussed Order ID."""
    # 1. Search recent chat history from latest to oldest
    for msg in reversed(chat_history):
        content = msg.get("content", "")
        match = re.search(r"\b(ORD-[A-Za-z0-9]+)\b", content, re.IGNORECASE)
        if match:
            return match.group(1).upper()

    # 2. Check customer's active orders
    if active_orders and len(active_orders) > 0:
        first_order = active_orders[0]
        oid = first_order.get("order_id") or first_order.get("id")
        if oid:
            return str(oid).upper()

    return None


def format_recent_context_window(chat_history: List[Dict[str, Any]], max_turns: int = 3) -> str:
    """Formats the last N turns for the reformulation prompt."""
    if not chat_history:
        return ""

    recent = chat_history[- (max_turns * 2):]
    lines = []
    for msg in recent:
        role = "Customer" if msg.get("role") == "user" else "Assistant"
        content = msg.get("content", "").strip()
        # Clean microphone emojis or formatting tags if present
        content = re.sub(r"^🎤\s*", "", content)
        lines.append(f"{role}: {content}")

    return "\n".join(lines)


def reformulate_query_llm(
    query_text: str,
    context_str: str,
    active_orders_hint: str = ""
) -> str:
    """Calls a high-speed LLM to rewrite the query into an unambiguous standalone search query."""
    system_prompt = (
        "You are an expert conversational query reformulation engine for an e-commerce support AI.\n"
        "Your sole task is to rewrite the customer's latest message into a clear, complete, and self-contained search query.\n\n"
        "Rules:\n"
        "1. Resolve all ambiguous pronouns ('it', 'that', 'they', 'this', 'them', 'the item') to the specific product, order, or service discussed in the conversation history.\n"
        "2. Expand elliptical follow-up questions (e.g. 'what about warranty?' -> 'what is the warranty policy for [Product]?').\n"
        "3. If the user refers to 'my order', 'the package', or 'tracking' and an Order ID or product is identified in history, include the exact Order ID or product name.\n"
        "4. Preserve the user's intent and language strictly. Do NOT answer the question.\n"
        "5. If the query is ALREADY standalone and unambiguous, output the original query verbatim.\n"
        "6. Output ONLY the rewritten query text. Do NOT provide quotes, explanations, markdown formatting, or preamble."
    )

    user_prompt = f"Conversation History:\n{context_str}\n"
    if active_orders_hint:
        user_prompt += f"\nKnown Active Customer Orders:\n{active_orders_hint}\n"
    user_prompt += f"\nCustomer Latest Query: \"{query_text}\"\n\nStandalone Reformulated Query:"

    models_to_try = [
        "openai/gpt-oss-20b",
        "qwen/qwen3.8-27b",
        LLM_MODEL,
        "openai/gpt-oss-120b"
    ]
    seen = set()
    unique_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

    client = get_groq_client()
    for model_name in unique_models:
        try:
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model=model_name,
                max_tokens=80,
                temperature=0.0,
            )
            raw = completion.choices[0].message.content or ""
            # Strip quotes or markdown that LLM might wrap
            cleaned = raw.strip().strip('"\'`')
            # Strip prefixes like "Reformulated Query:" or "Query:"
            cleaned = re.sub(r"^(?:Standalone\s*Reformulated\s*Query|Reformulated\s*Query|Query)\s*:\s*", "", cleaned, flags=re.IGNORECASE).strip()

            if cleaned:
                return cleaned
        except Exception as e:
            logger.warning(f"⚠️ Query reformulation attempt failed on {model_name}: {e}")

    return query_text


def reformulate_query(
    query_text: str,
    chat_history: Optional[List[Dict[str, Any]]] = None,
    active_orders: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Main entrypoint for Query Reformulation.

    Args:
        query_text: Raw incoming user utterance.
        chat_history: List of recent chat history dictionaries.
        active_orders: Optional list of customer's active orders.

    Returns:
        A standalone, disambiguated query string ready for vector retrieval.
    """
    if not query_text or not query_text.strip():
        return query_text

    clean_query = query_text.strip()
    history = chat_history or []

    # 1. Fast-Path Heuristic Check
    if not needs_reformulation(clean_query, history):
        return clean_query

    # 2. Check In-Memory Cache
    cache_key = f"{clean_query.lower()}||{len(history)}"
    if cache_key in _REFORMULATION_CACHE:
        return _REFORMULATION_CACHE[cache_key]

    # 3. Deterministic Order Resolution (Fast-Path for Tracking / Status)
    recent_order_id = extract_recent_order_id(history, active_orders)
    lower_query = clean_query.lower()
    is_order_inquiry = any(term in lower_query for term in ["my order", "the order", "track it", "where is it", "cancel it", "package status"])
    has_explicit_order = bool(re.search(r"\bORD-[A-Za-z0-9]+\b", clean_query, re.IGNORECASE))

    if is_order_inquiry and recent_order_id and not has_explicit_order:
        deterministic_rewrite = f"{clean_query} for order #{recent_order_id}"
        logger.info(f"🔄 Deterministic order injection: '{clean_query}' -> '{deterministic_rewrite}'")
        _REFORMULATION_CACHE[cache_key] = deterministic_rewrite
        return deterministic_rewrite

    # 4. Context Window Assembly
    context_str = format_recent_context_window(history, max_turns=3)
    if not context_str:
        return clean_query

    active_orders_hint = ""
    if active_orders:
        orders_summary = []
        for o in active_orders[:2]:
            oid = o.get("order_id") or o.get("id")
            pname = o.get("product_name") or (o.get("products") or {}).get("name") or "Product"
            orders_summary.append(f"Order #{oid}: {pname}")
        active_orders_hint = ", ".join(orders_summary)

    # 5. LLM-Based Reformulation
    try:
        reformulated = reformulate_query_llm(clean_query, context_str, active_orders_hint)
        if reformulated and reformulated.lower() != clean_query.lower():
            logger.info(f"🔄 [Query Reformulation] '{clean_query}' ➔ '{reformulated}'")
        else:
            reformulated = clean_query

        # Maintain cache bounds
        if len(_REFORMULATION_CACHE) >= _MAX_CACHE_SIZE:
            _REFORMULATION_CACHE.clear()
        _REFORMULATION_CACHE[cache_key] = reformulated

        return reformulated

    except Exception as e:
        logger.error(f"❌ Error during query reformulation: {e}", exc_info=True)
        return clean_query
