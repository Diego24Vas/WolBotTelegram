import asyncio
import logging
from telegram.ext import Application, CommandHandler

from config import settings
from database.db import init_db, checkpoint
from handlers.start import start
from handlers.version import version
from handlers.servers import servers_list, server_status, server_wake
from handlers.admin import add_server, remove_server, add_user, remove_user, list_users, server_info

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def error_handler(update, context):
    logger.error("Excepción no manejada: %s", context.error, exc_info=True)
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "Ocurrió un error inesperado. El bot seguirá funcionando."
        )


async def periodic_checkpoint():
    while True:
        await asyncio.sleep(300)
        try:
            await checkpoint()
            logger.debug("WAL checkpoint completado")
        except Exception as e:
            logger.warning("Error en WAL checkpoint: %s", e)


async def post_init(app):
    app.create_task(periodic_checkpoint())


def main():
    init_db()

    app = (
        Application.builder()
        .token(settings.BOT_TOKEN)
        .read_timeout(30)
        .get_updates_read_timeout(30)
        .post_init(post_init)
        .build()
    )

    app.add_error_handler(error_handler)

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("servers", servers_list))
    app.add_handler(CommandHandler("status", server_status))
    app.add_handler(CommandHandler("on", server_wake))
    app.add_handler(CommandHandler("add", add_server))
    app.add_handler(CommandHandler("remove", remove_server))
    app.add_handler(CommandHandler("adduser", add_user))
    app.add_handler(CommandHandler("removeuser", remove_user))
    app.add_handler(CommandHandler("users", list_users))
    app.add_handler(CommandHandler("info", server_info))
    app.add_handler(CommandHandler("version", version))

    logger.info("Bot iniciado...")
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
