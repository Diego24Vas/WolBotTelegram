# Wol Telegram Bot

Bot de Telegram para encender servidores remotamente mediante mensajes. Con base de datos SQLite, sistema de roles (admin/user), y gestión de servidores desde el chat.

---

## Requisitos

- Docker
- Token de bot de Telegram (de [@BotFather](https://t.me/BotFather))

---

## Instalación

### Con Docker (recomendado)

```bash
# Clonar el proyecto
git clone <repo> wakeOnLanBot
cd WolBotTelegram

# Crear archivo .env con tu token
echo "BOT_TOKEN=tu_token_de_botfather" > .env

# Iniciar el bot
docker compose up --build -d
```

---

## Agregar el primer admin

El bot arranca sin usuarios registrados. Ejecutá este script para agregarte como admin:

```bash
python scripts/add_admin.py

# Si ya has iniciado docker se ocupa este comando 
docker compose run --rm bot python scripts/add_admin.py
```

Te pedirá tu **ID de Telegram** (lo obtenés de [@userinfobot](https://t.me/userinfobot)) y opcionalmente un username.

Una vez agregado, desde el chat del bot podés agregar más usuarios con `/adduser`.

---

## Comandos

### Para todos los usuarios autorizados

| Comando              | Descripción                      |
| -------------------- | --------------------------------- |
| `/start`           | Mensaje de bienvenida             |
| `/servers`         | Listar servidores y su estado     |
| `/status <nombre>` | Estado de un servidor específico |
| `/on <nombre>`     | Encender un servidor por WoL      |

### Solo administradores

| Comando                      | Descripción                     |
| ---------------------------- | -------------------------------- |
| `/add <nombre> <MAC> <IP>` | Agregar un servidor              |
| `/remove <nombre>`         | Eliminar un servidor             |
| `/adduser <id>:<rol>`      | Agregar o cambiar rol de usuario |
| `/removeuser <id>`         | Eliminar usuario de la whitelist |

Ejemplos:

```
/add servidor1 AA:BB:CC:DD:EE:FF 192.168.1.100
/on servidor1
/adduser 123456789:admin
```

---

## Roles

| Rol   | Permisos                                            |
| ----- | --------------------------------------------------- |
| admin | Todos los comandos                                  |
| user  | Solo:`/servers`, `/status`, `/on`, `/start` |
