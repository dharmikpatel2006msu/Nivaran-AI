"""Supabase database client wrapper and initialization logic."""

import logging
from typing import Optional
from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_KEY

logger = logging.getLogger(__name__)

_supabase_client: Optional[Client] = None


def get_supabase_client() -> Client:
    """Initializes and returns the singleton Supabase client instance.

    Returns:
        Client: Configured Supabase Python SDK client.
    """
    global _supabase_client

    if _supabase_client is None:
        if not SUPABASE_URL or not SUPABASE_KEY:
            logger.warning("⚠️ SUPABASE_URL or SUPABASE_KEY missing in environment variables.")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ Supabase client initialized successfully.")

    return _supabase_client
