from telegram import Update
from telegram.ext import ContextTypes
from handlers.auth import authorized_only
from database.repository import (
    agregar_servidor,
    eliminar_servidor,
    obtener_servidor,
    registrar_usuario,
    actualizar_rol_usuario,
    eliminar_usuario,
    obtener_usuario,
    listar_usuarios,
    registrar_log,
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

    if obtener_servidor(nombre):
        await update.message.reply_text(f"El servidor '{nombre}' ya existe.")
        return

    agregar_servidor(nombre, mac, ip, puerto)
    await update.message.reply_text(f"Servidor '{nombre}' agregado.")
    registrar_log(update.effective_user.id, "/add", f"{nombre} {mac} {ip} {puerto}")


@authorized_only(min_rol="admin")
async def remove_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /remove <nombre>")
        return

    nombre = " ".join(context.args)
    if not obtener_servidor(nombre):
        await update.message.reply_text(f"Servidor '{nombre}' no encontrado.")
        return

    eliminar_servidor(nombre)
    await update.message.reply_text(f"Servidor '{nombre}' eliminado.")
    registrar_log(update.effective_user.id, "/remove", nombre)


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

    if obtener_usuario(user_id):
        actualizar_rol_usuario(user_id, rol)
    else:
        registrar_usuario(user_id, rol=rol)

    await update.message.reply_text(f"Usuario {user_id} configurado como {rol}.")
    registrar_log(update.effective_user.id, "/adduser", f"{user_id}:{rol}")


@authorized_only(min_rol="admin")
async def remove_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /removeuser <user_id>")
        return

    if not context.args[0].isdigit():
        await update.message.reply_text("Uso: /removeuser <user_id>")
        return

    user_id = int(context.args[0])
    if not obtener_usuario(user_id):
        await update.message.reply_text(f"Usuario {user_id} no encontrado.")
        return

    eliminar_usuario(user_id)
    await update.message.reply_text(f"Usuario {user_id} eliminado.")
    registrar_log(update.effective_user.id, "/removeuser", str(user_id))
