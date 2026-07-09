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
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /adduser <user_id> <nombre> [rol]\nEj: /adduser 123456789 Juan admin")
        return

    if not context.args[0].isdigit():
        await update.message.reply_text("El user_id debe ser numérico.\nUso: /adduser <user_id> <nombre> [rol]")
        return

    user_id = int(context.args[0])
    username = context.args[1]
    rol = context.args[2] if len(context.args) >= 3 and context.args[2] in ("admin", "user") else "user"

    if await obtener_usuario_async(user_id):
        await actualizar_rol_usuario_async(user_id, rol)
    else:
        await registrar_usuario_async(user_id, username=username, rol=rol)

    await update.message.reply_text(f"Usuario {user_id} ({username}) configurado como {rol}.")
    await registrar_log_async(update.effective_user.id, "/adduser", f"{user_id} {username} {rol}")


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
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = await listar_usuarios_async()
    if not users:
        await update.message.reply_text("No hay usuarios registrados.")
        return

    lines = [
        f"ID: {u['id']} | Usuario: {u['username'] or 'N/A'} | Rol: {u['rol']}"
        for u in users
    ]
    await update.message.reply_text("Usuarios registrados:\n\n" + "\n".join(lines))
    await registrar_log_async(update.effective_user.id, "/users", None)


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
