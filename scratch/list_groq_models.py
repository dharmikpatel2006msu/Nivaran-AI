import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from groq import Groq
from src.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
try:
    models = client.models.list()
    print("AVAILABLE GROQ MODELS:")
    for m in models.data:
        print(f"- {m.id}")
except Exception as e:
    print(f"Error: {e}")
