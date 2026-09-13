import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from groq import Groq
from src.config import GROQ_API_KEY
client = Groq(api_key=GROQ_API_KEY)

for model in ['qwen/qwen3.6-27b', 'openai/gpt-oss-120b', 'openai/gpt-oss-20b', 'groq/compound-mini']:
    try:
        res = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': 'You are a customer support assistant for ShopNest. Answer directly in 2 sentences.'},
                {'role': 'user', 'content': 'How do I return an item?'}
            ],
            max_tokens=250
        )
        content = res.choices[0].message.content or ""
        has_think = "<think>" in content
        print(f"=== Model: {model} ===")
        print(f"Has <think>? {has_think}")
        print(f"Content: {content.strip()[:160]}\n")
    except Exception as e:
        print(f"=== Model: {model} ERROR: {e}\n")
