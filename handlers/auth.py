from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

from database.repository import obtener_usuario


def authorized_only(min_rol: str = "user"):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            if not user:
                return None

            db_user = obtener_usuario(user.id)

            if db_user is None:
                await update.message.reply_text(
                    "No tienes permiso para usar este bot."
                )
                return None

            roles = {"admin": 2, "user": 1}
            if roles.get(db_user.get("rol", "user"), 0) < roles.get(min_rol, 1):
                await update.message.reply_text(
                    "No tienes permiso para usar este comando."
                )
                return None

            return await func(update, context)

        return wrapper
    return decorator
