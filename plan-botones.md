# Plan: Agregar botones inline al bot de Telegram

## Objetivo

Agregar botones (InlineKeyboardMarkup) para interactuar con el bot sin escribir comandos manualmente, **sin modificar la lógica existente** de los handlers. Los botones solo reutilizarán las funciones ya implementadas.

---

## 1. Visión general del menú

```
/start
 └── Menú Principal
      ├── 📋 Listar servidores    → (llama a servers_list internamente)
      ├── 🔌 Encender servidor    → (pregunta cuál, luego llama a server_wake)
      ├── 📊 Estado servidor      → (pregunta cuál, luego llama a server_status)
      ├── ℹ️ Info servidor (admin) → (pregunta cuál, luego llama a server_info)
      └── ⚙️ Admin (admin)
           ├── ➕ Añadir servidor  → (flujo: pide nombre, MAC, IP)
           ├── ❌ Eliminar servidor → (lista, confirma, llama a remove_server)
           ├── 👥 Listar usuarios   → (llama a list_users internamente)
           ├── ➕ Añadir usuario    → (flujo: pide ID, nombre, rol)
           ├── ❌ Eliminar usuario  → (flujo: pide ID, llama a remove_user)
           └── ◀️ Volver
```

---

## 2. Archivos nuevos

### `handlers/keyboards.py` — Definiciones de teclados

Funciones que devuelven `InlineKeyboardMarkup`:

- `main_menu(rol: str)` — menú principal (varía si admin o user)
- `server_list_menu(servidores: list, action_prefix: str)` — lista de servidores como botones, cada uno con `callback_data` tipo `"action:server_name"`
- `admin_menu()` — submenú de admin
- `confirm_menu(callback_yes: str, callback_no: str, message: str)` — confirmación sí/no
- `back_button(callback_data: str = "main_menu")` — botón volver

### `handlers/callbacks.py` — Manejadores de CallbackQuery

Funciones asíncronas decoradas con `@authorized_only` (vía `CallbackQueryHandler`):

| Botón | Handler | Lógica que reutiliza |
|---|---|---|
| `main_menu` | `menu_main` | Muestra menú principal |
| `admin_menu` | `menu_admin` | Muestra submenú admin |
| `server_list` | `menu_servers` | `servers_list` (misma lógica, envía resultado como reply) |
| `server_status:<nombre>` | `menu_server_status` | `server_status` (misma lógica) |
| `server_wake:<nombre>` | `menu_server_wake` | `server_wake` (misma lógica) |
| `server_info:<nombre>` | `menu_server_info` | `server_info` (misma lógica) |
| `server_add` | `menu_server_add_start` | Inicia flujo de add server (usa `ConversationHandler` o states) |
| `server_remove:<nombre>` | `menu_server_remove` | `remove_server` (misma lógica) |
| `user_list` | `menu_users` | `list_users` (misma lógica) |
| `user_add` | `menu_user_add_start` | Inicia flujo de add user |
| `user_remove` | `menu_user_remove_start` | Inicia flujo de remove user |
| `confirm:yes` | `menu_confirm_yes` | Confirma acción destructiva |
| `confirm:no` | `menu_confirm_no` | Cancela acción |

### Patrón para reutilizar lógica existente

```python
# En lugar de duplicar código, llamamos a la función original
# adaptando update/context para que funcione con callback
async def menu_server_status(update, context):
    query = update.callback_query
    await query.answer()
    server_name = query.data.split(":", 1)[1]
    # Reconstruimos args para llamar al handler original
    context.args = [server_name]
    await server_status(update, context)  # ← reutiliza handler original
```

Esto puede requerir ajustar los handlers existentes para que funcionen tanto con `update.message` como con `update.callback_query`. Se hará con un helper mínimo (ver sección 4).

---

## 3. Cambios a archivos existentes

### `main.py`

```diff
- from handlers import start, version, servers, admin
+ from handlers import start, version, servers, admin, callbacks

  app.add_handler(CommandHandler("start", start.start))
  # ... otros handlers ...

+ # CallbackQueryHandlers para menú
+ app.add_handler(CallbackQueryHandler(callbacks.menu_main, pattern="^main_menu$"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_admin, pattern="^admin_menu$"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_servers, pattern="^servers_list$"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_server_status, pattern="^server_status:"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_server_wake, pattern="^server_wake:"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_server_info, pattern="^server_info:"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_server_add, pattern="^server_add$"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_server_remove_select, pattern="^server_remove_list$"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_server_remove, pattern="^server_remove:"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_users, pattern="^users_list$"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_user_add, pattern="^user_add$"))
+ app.add_handler(CallbackQueryHandler(callbacks.menu_user_remove, pattern="^user_remove$"))

- app.run_polling(allowed_updates=["message"])
+ app.run_polling(allowed_updates=["message", "callback_query"])
```

### `handlers/start.py`

```diff
- await update.message.reply_text(help_text)
+ await update.message.reply_text(help_text, reply_markup=main_menu(rol))
```

### `handlers/auth.py` (opcional)

Agregar un wrapper `@authorized_callback` o reutilizar `authorized_only` adaptándolo para `CallbackQuery`.

---

## 4. Helper para dualidad message/callback

Se creará `utils/responder.py` con funciones que abstraen si responder a `message` o `callback_query`:

```python
async def reply(update, text, **kwargs):
    if update.callback_query:
        q = update.callback_query
        await q.edit_message_text(text, **kwargs)
    else:
        await update.message.reply_text(text, **kwargs)

async def edit_or_reply(update, text, **kwargs):
    if update.callback_query:
        q = update.callback_query
        await q.edit_message_text(text, **kwargs)
    else:
        await update.message.reply_text(text, **kwargs)
```

Esto permite que los handlers existentes funcionen sin cambios cuando son invocados desde un callback.

---

## 5. Módulo de flujos conversacionales (opcional pero recomendado)

Para acciones que requieren múltiples pasos (add server, add user, remove user) se puede usar `ConversationHandler` de PTB con estados:

```
server_add → STATE_SERVER_NAME → STATE_SERVER_MAC → STATE_SERVER_IP → done
user_add   → STATE_USER_ID → STATE_USER_NAME → STATE_USER_ROLE → done
user_remove → STATE_USER_ID → done
```

Esto mantiene la lógica separada de los handlers existentes.

---

## 6. Resumen de cambios totales

| Archivo | Tipo de cambio |
|---|---|
| `handlers/keyboards.py` | **Nuevo** — definiciones de teclados |
| `handlers/callbacks.py` | **Nuevo** — manejadores de callback |
| `utils/responder.py` | **Nuevo** — helper message/callback |
| `handlers/start.py` | **Modificar** — agregar `reply_markup=` |
| `main.py` | **Modificar** — registrar handlers + callback queries |

**Lo que NO se toca:**
- `handlers/servers.py` (lógica intacta, solo se reutiliza)
- `handlers/admin.py` (lógica intacta, solo se reutiliza)
- `services/` (sin cambios)
- `database/` (sin cambios)
- `models.py` (sin cambios)
- Tests existentes (sin cambios)

---

## 7. Orden de implementación

1. Crear `utils/responder.py` (helper message/callback) — sin dependencias
2. Crear `handlers/keyboards.py` (definiciones de teclados) — depende solo de python-telegram-bot
3. Crear `handlers/callbacks.py` (manejadores) — depende de keyboards, responder, auth, handlers existentes
4. Modificar `handlers/start.py` — agregar menú
5. Modificar `main.py` — registrar todo
6. Probar manualmente
