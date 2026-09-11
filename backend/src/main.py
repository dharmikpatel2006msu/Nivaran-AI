"""FastAPI Application Entrypoint for Nivaran AI Backend.

Wires REST Admin endpoints, database connection initialization,
and Telegram Bot polling background service lifecycle.
"""

import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import PORT, HOST, TELEGRAM_BOT_TOKEN
from src.api.admin_routes import router as admin_router
from src.integrations.telegram_client import setup_telegram_application

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

telegram_app = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifespan Context Manager for background services initialization."""
    logger.info("⚡ Nivaran AI Backend initializing...")
    global telegram_app

    # Start Telegram Bot Polling in background if token is configured
    if TELEGRAM_BOT_TOKEN:
        try:
            telegram_app = setup_telegram_application()
            if telegram_app:
                await telegram_app.initialize()
                await telegram_app.start()
                await telegram_app.updater.start_polling()
                logger.info("🚀 Telegram Bot polling service running.")
        except Exception as e:
            logger.error(f"❌ Failed to start Telegram Bot polling: {e}")
    else:
        logger.warning("⚠️ Running in REST API mode only (TELEGRAM_BOT_TOKEN not provided).")

    yield  # Server runs here

    # Shutdown hooks
    logger.info("🛑 Nivaran AI Backend shutting down...")
    if telegram_app and telegram_app.updater and telegram_app.updater.running:
        await telegram_app.updater.stop()
        await telegram_app.stop()
        await telegram_app.shutdown()
        logger.info("👋 Telegram Bot polling stopped.")


app = FastAPI(
    title="Nivaran AI Backend API",
    description="Python FastAPI backend powering RAG Customer Support and Admin Panel integrations.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Frontend Admin Panel development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust allowed origins for production deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Admin REST API Routes
app.include_router(admin_router)


@app.get("/", tags=["Health Check"])
async def root():
    """Root status endpoint."""
    return {
        "service": "Nivaran AI Backend",
        "status": "online",
        "version": "1.0.0",
        "docs_url": "/docs"
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on http://{HOST}:{PORT}")
    uvicorn.run("src.main:app", host=HOST, port=PORT, reload=True)
