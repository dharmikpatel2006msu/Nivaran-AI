"""LLM text generator module for Nivaran AI RAG pipeline.

Ported from Node.js prototype (`index.js` lines 98-116).
Original logic:
- Groq SDK with `qwen/qwen3.6-27b` model.
- Removes internal thinking tags (`<think>...</think>`).
"""

import re
import logging
from typing import List, Dict, Any
from groq import Groq
from src.config import GROQ_API_KEY, LLM_MODEL
from src.system_prompt import build_system_prompt

logger = logging.getLogger(__name__)

_groq_client = None


def get_groq_client() -> Groq:
    """Initializes and returns the Groq API client."""
    global _groq_client
    if _groq_client is None:
        _groq_client = Groq(api_key=GROQ_API_KEY)
    return _groq_client


def clean_llm_output(raw_text: str) -> str:
    """Removes thinking tags, draft headers, and chain-of-thought scratchpad blocks."""
    if not raw_text:
        return ""

    # 1. Remove XML/HTML thinking tags (<think>...</think>) or unclosed (<think>...)
    text = re.sub(r"<think>[\s\S]*?(?:<\/think>|$)", "", raw_text, flags=re.IGNORECASE).strip()

    # 2. If <think> tags were stripped and emptied text, fallback to removing just tags
    if not text:
        text = re.sub(r"<\/?think>", "", raw_text, flags=re.IGNORECASE).strip()

    # 3. Strip leading draft / reasoning section headers if present
    # Examples: "4. **Draft Response**\n", "**Draft Response:**", "Draft Response:"
    text = re.sub(
        r"^(?:(?:\d+\.|\*|-)?\s*\*{0,2}(?:Draft Response|Final Response|Response|Answer|Customer Response)\*{0,2}:?\s*)+",
        "",
        text,
        flags=re.IGNORECASE
    ).strip()

    # 4. Remove leading constraint check / thinking bullet points if any remain at start
    # e.g., "- Constraint check: ... \n\n"
    text = re.sub(
        r"^(?:[-*]\s*(?:Constraint check|Thinking|Analysis|Context check)[\s\S]*?\n\n)+",
        "",
        text,
        flags=re.IGNORECASE
    ).strip()

    return text


def generate_llm_response(
    user_message: str,
    context_documents: List[Dict[str, Any]],
    chat_history_formatted: str = "",
    active_orders_formatted: str = ""
) -> str:
    """Generates a contextual response using Groq LLMs with automatic fallbacks.

    Args:
        user_message: Incoming user text query.
        context_documents: Retrieved knowledge docs from pgvector.
        chat_history_formatted: Formatted recent conversation window string.
        active_orders_formatted: Formatted list of customer active orders.

    Returns:
        Cleaned LLM response text.
    """
    context_text = "\n\n".join([doc.get("content", "") for doc in context_documents]) if context_documents else ""
    system_prompt = build_system_prompt(context_text, chat_history_formatted, active_orders_formatted)

    models_to_try = [
        LLM_MODEL,
        "openai/gpt-oss-120b",
        "qwen/qwen3.8-27b",
        "qwen/qwen3.6-27b",
        "openai/gpt-oss-20b",
        "groq/compound-mini"
    ]
    # Remove duplicates while preserving order
    seen = set()
    unique_models = [m for m in models_to_try if not (m in seen or seen.add(m))]

    client = get_groq_client()
    last_error = None

    for model_name in unique_models:
        try:
            logger.info(f"🤖 Invoking Groq LLM model ({model_name})...")
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                model=model_name,
                max_tokens=1024,
                temperature=0.2,
            )

            response_content = completion.choices[0].message.content or ""
            cleaned_response = clean_llm_output(response_content)

            if cleaned_response:
                logger.info(f"💡 Generated response ({model_name}): '{cleaned_response[:80]}...'")
                return cleaned_response

        except Exception as e:
            logger.warning(f"⚠️ Groq LLM generation failed with {model_name}: {e}")
            last_error = e

    logger.error(f"❌ All Groq LLM model attempts failed: {last_error}")
    return "I apologize, but I encountered an issue retrieving the information. Our customer support team has been notified to assist you."
