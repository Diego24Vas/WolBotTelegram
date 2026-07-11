from telegram import ReplyKeyboardMarkup


def main_menu(rol: str) -> ReplyKeyboardMarkup:
    keyboard = [
        ["📋 Servidores"],
        ["🔌 Encender", "📊 Estado"],
    ]
    if rol == "admin":
        keyboard.append(["🖥️ Servidor"])
        keyboard.append(["👤 Usuario"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def server_submenu() -> ReplyKeyboardMarkup:
    keyboard = [
        ["ℹ️ Info", "➕ Añadir", "❌ Eliminar"],
        ["◀️ Volver"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def user_submenu() -> ReplyKeyboardMarkup:
    keyboard = [
        ["👥 Listar", "➕ Añadir", "❌ Eliminar"],
        ["◀️ Volver"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def server_list_keyboard(servers: list) -> ReplyKeyboardMarkup:
    keyboard = [[s["nombre"]] for s in servers]
    keyboard.append(["◀️ Volver"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
