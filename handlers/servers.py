from telegram import Update
from telegram.ext import ContextTypes
from handlers.auth import authorized_only
from database.repository import listar_servidores, obtener_servidor, registrar_log
from services.ping import ping_host
from services.wol import send_wol
from utils.helpers import format_mac, server_status_emoji, server_status_text


@authorized_only()
async def servers_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servers = listar_servidores()
    if not servers:
        await update.message.reply_text("No hay servidores configurados.")
        return

    lines = []
    for srv in servers:
        alive = ping_host(srv["ip"])
        lines.append(f"{server_status_emoji(alive)} {srv['nombre']} - {server_status_text(alive)}")

    await update.message.reply_text("Servidores:\n" + "\n".join(lines))
    registrar_log(update.effective_user.id, "/servers")


@authorized_only()
async def server_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /status <nombre del servidor>")
        return

    nombre = " ".join(context.args)
    srv = obtener_servidor(nombre)
    if not srv:
        await update.message.reply_text(f"Servidor '{nombre}' no encontrado.")
        return

    alive = ping_host(srv["ip"])
    await update.message.reply_text(
        f"{srv['nombre']}: {server_status_emoji(alive)} {server_status_text(alive)}"
    )
    registrar_log(update.effective_user.id, "/status", nombre)


@authorized_only()
async def server_wake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /on <nombre del servidor>")
        return

    nombre = " ".join(context.args)
    srv = obtener_servidor(nombre)
    if not srv:
        await update.message.reply_text(f"Servidor '{nombre}' no encontrado.")
        return

    await update.message.reply_text(f"Enviando paquete WoL a {srv['nombre']}...")
    success = send_wol(srv["mac"], srv["ip"], srv["puerto"])

    if success:
        await update.message.reply_text(f"Paquete WoL enviado a {srv['nombre']}.")
    else:
        await update.message.reply_text(f"Error al enviar WoL a {srv['nombre']}.")

    registrar_log(update.effective_user.id, "/on", nombre)
