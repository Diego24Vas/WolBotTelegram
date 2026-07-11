from telegram import Update
from telegram.ext import ContextTypes

from handlers.auth import authorized_only
from handlers.keyboards import main_menu, server_submenu, user_submenu, server_list_keyboard
from handlers.servers import servers_list, server_status, server_wake
from handlers.admin import server_info, remove_server, list_users
from database.repository import listar_servidores_async, obtener_servidor_async, obtener_usuario_async

_MENU_TEXTS = {
    "📋 Servidores", "🔌 Encender", "📊 Estado",
    "🖥️ Servidor", "👤 Usuario",
    "ℹ️ Info", "➕ Añadir", "❌ Eliminar",
    "👥 Listar",
    "◀️ Volver",
}


@authorized_only()
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    state = context.user_data.get("menu_state")

    if text == "◀️ Volver":
        context.user_data.pop("menu_state", None)
        await _show_main(update, context)
        return

    if state is None:
        if text not in _MENU_TEXTS:
            return
        await _handle_main(update, context, text)
    elif state in ("server_sub", "user_sub"):
        await _handle_sub(update, context, text, state)
    else:
        await _handle_selection(update, context, text, state)


async def _show_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await obtener_usuario_async(update.effective_user.id)
    rol = user.get("rol", "user") if user else "user"
    await update.message.reply_text("Menú principal:", reply_markup=main_menu(rol))


async def _handle_main(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    if text == "📋 Servidores":
        await servers_list(update, context)
    elif text == "🔌 Encender":
        await _pick_server(update, context, "wake", "Seleccioná un servidor para encender:")
    elif text == "📊 Estado":
        await _pick_server(update, context, "status", "Seleccioná un servidor para ver su estado:")
    elif text == "🖥️ Servidor":
        context.user_data["menu_state"] = "server_sub"
        await update.message.reply_text("Gestión de servidores:", reply_markup=server_submenu())
    elif text == "👤 Usuario":
        context.user_data["menu_state"] = "user_sub"
        await update.message.reply_text("Gestión de usuarios:", reply_markup=user_submenu())


async def _handle_sub(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, sub: str):
    if sub == "server_sub":
        if text == "ℹ️ Info":
            await _pick_server(update, context, "info", "Seleccioná un servidor para ver su info:")
        elif text == "➕ Añadir":
            await update.message.reply_text(
                "Usá el comando /add nombre MAC IP\n"
                "Ej: /add server1 AA:BB:CC:DD:EE:FF 192.168.1.100"
            )
        elif text == "❌ Eliminar":
            await _pick_server(update, context, "remove", "Seleccioná un servidor para eliminar:")
    elif sub == "user_sub":
        if text == "👥 Listar":
            await list_users(update, context)
        elif text == "➕ Añadir":
            await update.message.reply_text(
                "Usá el comando /adduser id nombre [rol]\n"
                "Ej: /adduser 123456789 juan admin"
            )
        elif text == "❌ Eliminar":
            await update.message.reply_text(
                "Usá el comando /removeuser id\n"
                "Ej: /removeuser 123456789"
            )


async def _pick_server(update: Update, context: ContextTypes.DEFAULT_TYPE, action: str, msg: str):
    servers = await listar_servidores_async()
    if not servers:
        await update.message.reply_text("No hay servidores configurados.")
        return
    context.user_data["menu_state"] = action
    await update.message.reply_text(msg, reply_markup=server_list_keyboard(servers))


async def _handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, action: str):
    srv = await obtener_servidor_async(text)
    if not srv:
        await update.message.reply_text(f"Servidor '{text}' no encontrado.")
        return

    context.args = [text]
    if action == "wake":
        await server_wake(update, context)
    elif action == "status":
        await server_status(update, context)
    elif action == "info":
        await server_info(update, context)
    elif action == "remove":
        await remove_server(update, context)

    context.user_data.pop("menu_state", None)
    await _show_main(update, context)
