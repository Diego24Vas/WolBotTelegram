from telegram.ext import Application, CommandHandler

from config import settings
from database.db import init_db
from handlers.start import start
from handlers.servers import servers_list, server_status, server_wake
from handlers.admin import add_server, remove_server, add_user, remove_user


def main():
    init_db()

    app = Application.builder().token(settings.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("servers", servers_list))
    app.add_handler(CommandHandler("status", server_status))
    app.add_handler(CommandHandler("on", server_wake))
    app.add_handler(CommandHandler("add", add_server))
    app.add_handler(CommandHandler("remove", remove_server))
    app.add_handler(CommandHandler("adduser", add_user))
    app.add_handler(CommandHandler("removeuser", remove_user))

    print("Bot iniciado...")
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
