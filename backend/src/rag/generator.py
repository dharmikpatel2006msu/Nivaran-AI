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


def generate_llm_response(
    user_message: str,
    context_documents: List[Dict[str, Any]],
    chat_history_formatted: str = ""
) -> str:
    """Generates a contextual response using Groq LLM (qwen/qwen3.6-27b).

    Ported from `index.js` lines 98-116:
    ```js
    const completion = await groq.chat.completions.create({
      messages: [...],
      model: 'qwen/qwen3.6-27b',
      max_tokens: 300,
    });
    ```

    Args:
        user_message: Incoming user text query.
        context_documents: Retrieved knowledge docs from pgvector.
        chat_history_formatted: Formatted recent conversation window string.

    Returns:
        Cleaned LLM response text.
    """
    context_text = "\n\n".join([doc.get("content", "") for doc in context_documents]) if context_documents else ""
    system_prompt = build_system_prompt(context_text, chat_history_formatted)

    logger.info(f"🤖 Invoking Groq LLM model ({LLM_MODEL})...")

    try:
        client = get_groq_client()
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            model=LLM_MODEL,
            max_tokens=450,
            temperature=0.2,
        )

        response_content = completion.choices[0].message.content or ""
        
        # Remove any internal reasoning thinking blocks output by qwen/reasoning models
        cleaned_response = re.sub(r"<think>[\s\S]*?(?:<\/think>|$)", "", response_content, flags=re.IGNORECASE).strip()
        logger.info(f"💡 Generated response: '{cleaned_response[:80]}...'")
        return cleaned_response

    except Exception as e:
        logger.error(f"❌ Groq LLM generation error: {e}")
        return "I apologize, but I encountered an error processing your request. Our human support team has been notified."
