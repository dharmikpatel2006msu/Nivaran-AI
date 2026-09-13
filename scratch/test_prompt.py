import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from src.rag.retriever import retrieve_context
from src.rag.generator import generate_llm_response

query = "How do I return an item?"
docs, sim = retrieve_context(query)
print(f"Docs retrieved: {len(docs)}, Max Sim: {sim}")
response = generate_llm_response(query, docs)
print("=== Response ===")
print(response)
