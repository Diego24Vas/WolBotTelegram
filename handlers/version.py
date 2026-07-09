from telegram import Update
from telegram.ext import ContextTypes

from config import __version__


async def version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"WolBotTelegram v{__version__}")