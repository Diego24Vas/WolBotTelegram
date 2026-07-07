from telegram import Update
from telegram.ext import ContextTypes
from handlers.auth import authorized_only


@authorized_only()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from database.repository import obtener_usuario
    user = obtener_usuario(update.effective_user.id)
    rol = user.get("rol", "user") if user else "user"

    base_text = (
        "Bot de encendido remoto.\n\n"
        "Comandos disponibles:\n"
        "/servers - Listar servidores y su estado\n"
        "/status <nombre> - Estado de un servidor\n"
        "/on <nombre> - Encender un servidor\n"
    )

    admin_text = (
        "/add <nombre> <MAC> <IP> - Agregar servidor\n"
        "/remove <nombre> - Eliminar servidor\n"
        "/adduser <user_id>:<rol> - Agregar/modificar usuario\n"
        "/removeuser <user_id> - Eliminar usuario\n"
    )

    if rol == "admin":
        await update.message.reply_text(base_text + "\nComandos de administración:\n" + admin_text)
    else:
        await update.message.reply_text(base_text)
