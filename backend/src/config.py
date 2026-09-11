"""Configuration and settings module for Nivaran AI Backend."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Server & General Config ---
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")

# --- API Keys & Credentials ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# --- Database & Supabase Config ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")

# --- RAG & AI Model Configuration ---
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 768
LLM_MODEL = "qwen/qwen3.6-27b"

# --- Conversational Memory Window ---
# Configurable window size for fetching previous messages for short-term chat context
CHAT_HISTORY_WINDOW = 5  # Exposed constant (range 5-10 recommended)

# --- Escalation & Confidence Thresholds ---
# TODO: Team input needed — tune SIMILARITY_THRESHOLD based on production knowledge precision
SIMILARITY_THRESHOLD = 0.5

# TODO: Team input needed — adjust LOW_CONFIDENCE_THRESHOLD for automatic ticket generation
LOW_CONFIDENCE_THRESHOLD = 0.45

# TODO: Team input needed — confirm consecutive unhelpful responses before escalation trigger
REPEATED_UNRESOLVED_THRESHOLD = 3
