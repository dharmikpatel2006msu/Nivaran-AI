"""Telegram Bot Client integration for Nivaran AI.

Ported from Node.js prototype (`index.js` lines 48-135).
Uses python-telegram-bot async application runner in long polling mode.
"""

import logging
import asyncio
from typing import Optional
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.config import TELEGRAM_BOT_TOKEN
from src.services.chat_service import process_incoming_message

logger = logging.getLogger(__name__)

_telegram_app: Optional[Application] = None


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler for Telegram /start command.

    Ported from `index.js` lines 50-54:
    ```js
    bot.command('start', (ctx) => {
        ctx.reply("👋 Hello! I am Nivaran AI Support Assistant...");
    });
    ```
    """
    welcome_text = (
        "👋 Hello! I am Nivaran AI Support Assistant.\n\n"
        "Ask me any question about our services, store hours, returns, or order tracking!"
    )
    if update.message:
        await update.message.reply_text(welcome_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Main message handler for incoming Telegram messages.

    Ported from `index.js` lines 57-131:
    - Extracts sender info and text.
    - Delegates processing to `process_incoming_message`.
    - Sends response reply to Telegram user.
    """
    if not update.message or not update.message.text:
        return

    incoming_msg = update.message.text.strip()
    if incoming_msg.startswith('/'):
        return

    user = update.effective_user
    telegram_id = user.id if user else 0
    display_name = user.full_name if user else "User"

    logger.info(f"\n📩 Incoming Telegram message from {display_name} ({telegram_id}): '{incoming_msg}'")

    try:
        # Show typing status in Telegram chat
        if update.effective_chat:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

        # Run chat service pipeline asynchronously in threadpool
        reply_text = await asyncio.to_thread(
            process_incoming_message,
            telegram_id,
            display_name,
            incoming_msg
        )

        if not reply_text or not reply_text.strip():
            reply_text = (
                "Hello! I'm here to help you with any questions about ShopNest orders, "
                "shipping options, return policies, or store hours. How can I assist you?"
            )

        logger.info(f"📤 Sending Telegram reply to {display_name}...")
        await update.message.reply_text(reply_text)
        logger.info("✅ Telegram reply sent successfully.")
    except Exception as e:
        logger.error(f"❌ Error handling Telegram message: {e}", exc_info=True)
        await update.message.reply_text(
            "I apologize, but I'm having trouble processing that request right now. "
            "Please try asking again, or let me know if you need help with returns, shipping, or order tracking."
        )


def setup_telegram_application() -> Optional[Application]:
    """Builds and configures the Telegram Bot application."""
    global _telegram_app

    if not TELEGRAM_BOT_TOKEN:
        logger.warning("⚠️ TELEGRAM_BOT_TOKEN is missing in environment variables!")
        logger.warning("👉 Add TELEGRAM_BOT_TOKEN=your_token_here to backend/.env")
        return None

    try:
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        _telegram_app = app
        logger.info("🚀 Telegram Bot Application configured successfully.")
        return app
    except Exception as e:
        logger.error(f"❌ Error initializing Telegram application: {e}")
        return None


async def start_telegram_polling() -> None:
    """Starts Telegram Bot polling background loop."""
    app = setup_telegram_application()
    if app:
        logger.info("🚀 Starting Telegram Bot polling loop...")
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
