from telegram import Update
from telegram.ext import ContextTypes
from handlers.auth import authorized_only
from database.repository import (
    agregar_servidor_async,
    eliminar_servidor_async,
    obtener_servidor_async,
    registrar_usuario_async,
    actualizar_rol_usuario_async,
    eliminar_usuario_async,
    obtener_usuario_async,
    listar_usuarios_async,
    registrar_log_async,
)


@authorized_only(min_rol="admin")
async def add_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text(
            "Uso: /add <nombre> <MAC> <IP>\n"
            "Ej: /add server1 AA:BB:CC:DD:EE:FF 192.168.1.100"
        )
        return

    nombre = context.args[0]
    mac = context.args[1]
    ip = context.args[2]
    puerto = 9

    if await obtener_servidor_async(nombre):
        await update.message.reply_text(f"El servidor '{nombre}' ya existe.")
        return

    await agregar_servidor_async(nombre, mac, ip, puerto)
    await update.message.reply_text(f"Servidor '{nombre}' agregado.")
    await registrar_log_async(update.effective_user.id, "/add", f"{nombre} {mac} {ip} {puerto}")


@authorized_only(min_rol="admin")
async def remove_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /remove <nombre>")
        return

    nombre = " ".join(context.args)
    if not await obtener_servidor_async(nombre):
        await update.message.reply_text(f"Servidor '{nombre}' no encontrado.")
        return

    await eliminar_servidor_async(nombre)
    await update.message.reply_text(f"Servidor '{nombre}' eliminado.")
    await registrar_log_async(update.effective_user.id, "/remove", nombre)


@authorized_only(min_rol="admin")
async def add_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /adduser <user_id>:<rol>")
        return

    parts = context.args[0].split(":")
    if len(parts) < 1 or not parts[0].isdigit():
        await update.message.reply_text("Formato inválido. Uso: /adduser <user_id>:<rol>")
        return

    user_id = int(parts[0])
    rol = parts[1] if len(parts) >= 2 and parts[1] in ("admin", "user") else "user"

    if await obtener_usuario_async(user_id):
        await actualizar_rol_usuario_async(user_id, rol)
    else:
        await registrar_usuario_async(user_id, rol=rol)

    await update.message.reply_text(f"Usuario {user_id} configurado como {rol}.")
    await registrar_log_async(update.effective_user.id, "/adduser", f"{user_id}:{rol}")


@authorized_only(min_rol="admin")
async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /removeuser <user_id>")
        return

    if not context.args[0].isdigit():
        await update.message.reply_text("Uso: /removeuser <user_id>")
        return

    user_id = int(context.args[0])
    if not await obtener_usuario_async(user_id):
        await update.message.reply_text(f"Usuario {user_id} no encontrado.")
        return

    await eliminar_usuario_async(user_id)
    await update.message.reply_text(f"Usuario {user_id} eliminado.")
    await registrar_log_async(update.effective_user.id, "/removeuser", str(user_id))


@authorized_only(min_rol="admin")
async def server_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /info <nombre del servidor>")
        return

    nombre = " ".join(context.args)
    srv = await obtener_servidor_async(nombre)
    if not srv:
        await update.message.reply_text(f"Servidor '{nombre}' no encontrado.")
        return

    await update.message.reply_text(
        f"{srv['nombre']}\n"
        f"MAC: {srv['mac']}\n"
        f"IP: {srv['ip']}\n"
        f"Puerto WoL: {srv['puerto']}"
    )
    await registrar_log_async(update.effective_user.id, "/info", nombre)
