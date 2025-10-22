import os
import random
import uuid
import logging
from typing import List

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Application, ContextTypes, InlineQueryHandler, CommandHandler


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

PUNCTUATION_VARIANTS: List[str] = [
    "!",
    "!!",
    "...",
    "?",
    "?!",
    "—",
    "…",
    "!!!",
    "?!?",
    "!?",
]


def generate_1536_sequence(num_tokens: int) -> str:
    parts: List[str] = []
    for _ in range(num_tokens):
        suffix = random.choice(PUNCTUATION_VARIANTS)
        parts.append(f"1536{suffix}")
    return " ".join(parts)


async def on_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.inline_query is None:
        return

    _ = context  # intentionally unused

    # Build 6 inline results with 1536 repeated 5..10 times and varied punctuation.
    results: List[InlineQueryResultArticle] = []

    for count in range(5, 11):
        text = generate_1536_sequence(count)
        results.append(
            InlineQueryResultArticle(
                id=f"{count}-{uuid.uuid4()}",
                title=f"1536 × {count}",
                description=(text[:80] + ("…" if len(text) > 80 else "")),
                input_message_content=InputTextMessageContent(text),
            )
        )

    await update.inline_query.answer(results, cache_time=0, is_personal=True)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text(
            "hi"
        )


async def on_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("get fucked by %s", update, exc_info=context.error)


def build_application() -> Application:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "u forgot token lol"
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(InlineQueryHandler(on_inline_query))
    application.add_error_handler(on_error)

    return application


if __name__ == "__main__":
    logger.info("swag number inline runs")
    app = build_application()
    app.run_polling(allowed_updates=Update.ALL_TYPES)
