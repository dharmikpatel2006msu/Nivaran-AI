import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from groq import Groq
from src.config import GROQ_API_KEY
from src.system_prompt import build_system_prompt
from src.rag.retriever import retrieve_context

client = Groq(api_key=GROQ_API_KEY)
query = "How do I return an item?"
docs, sim = retrieve_context(query)
context_text = "\n\n".join([d.get("content", "") for d in docs])
prompt = build_system_prompt(context_text, "")

for model in ["openai/gpt-oss-120b", "openai/gpt-oss-20b", "groq/compound-mini"]:
    print(f"\n--- Testing {model} ---")
    try:
        completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ],
            model=model,
            max_tokens=400,
            temperature=0.2
        )
        content = completion.choices[0].message.content or ""
        print("Length:", len(content))
        print("Response:\n", content)
    except Exception as e:
        print("Error:", e)
