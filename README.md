# WolBotTelegram v0.2.0

Bot de Telegram para encender servidores de forma remota mediante **Wake-on-LAN (WoL)**. Incluye menú interactivo por botones, base de datos SQLite, sistema de roles (admin/user), registro de actividad y gestión completa desde el chat.

---

## Requisitos

- **Docker** y **Docker Compose**
- Token de bot de Telegram (obtenélo de [@BotFather](https://t.me/BotFather))
- Los servidores destino deben tener **WoL habilitado en BIOS/UEFI** y en la interfaz de red

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repo> && cd WolBotTelegram
```

### 2. Configurar variables de entorno

```bash
# Crear el archivo .env (usá .env.example como referencia)
echo "BOT_TOKEN=tu_token_de_botfather" > .env
```

Variables disponibles:

| Variable          | Descripción                    | Obligatorio | Default         |
| ----------------- | ------------------------------- | ----------- | --------------- |
| `BOT_TOKEN`     | Token del bot de Telegram       | ✅          | —              |
| `DATABASE_PATH` | Ruta de la base de datos SQLite | ❌          | `data/bot.db` |

### 3. Iniciar el bot

```bash
docker compose up --build -d
```

> **Importante:** El `docker-compose.yml` usa `network_mode: host`. Esto es **necesario** para que los paquetes WoL lleguen a la red local. Sin esto, el broadcast de WoL no funcionará.

Para ver los logs:

```bash
docker compose logs -f
```

---

## Primeros pasos

El bot arranca sin usuarios registrados. Hay que agregar el primer admin manualmente:

```bash
# Si el bot corre en Docker:
docker compose run --rm bot python scripts/add_admin.py

# Si ejecutás sin Docker (solo para el script):
python scripts/add_admin.py
```

Te pedirá tu **ID de Telegram** (obtenélo de [@userinfobot](https://t.me/userinfobot)) y opcionalmente un username.

Una vez agregado, desde el chat del bot podés agregar más usuarios con `/adduser` o desde el menú.

---

## Comandos

### Para todos los usuarios autorizados

| Comando              | Descripción                                |
| -------------------- | ------------------------------------------- |
| `/start`           | Mensaje de bienvenida + menú interactivo   |
| `/servers`         | Listar servidores con estado online/offline |
| `/status <nombre>` | Estado de un servidor específico           |
| `/on <nombre>`     | Encender un servidor por WoL                |
| `/version`         | Versión actual del bot                     |

### Solo administradores

| Comando                          | Descripción                              |
| -------------------------------- | ----------------------------------------- |
| `/add <nombre> <MAC> <IP>`     | Agregar un servidor                       |
| `/remove <nombre>`             | Eliminar un servidor                      |
| `/adduser <id> <nombre> [rol]` | Agregar o modificar usuario               |
| `/removeuser <id>`             | Eliminar un usuario                       |
| `/users`                       | Listar todos los usuarios registrados     |
| `/info <nombre>`               | Detalles de un servidor (MAC, IP, puerto) |

### Ejemplos

```
/add servidor1 AA:BB:CC:DD:EE:FF 192.168.1.100
/on servidor1
/adduser 123456789 admin
/info servidor1
```

---

## Menú interactivo

Además de los comandos de texto, el bot ofrece un **menú con botones** (ReplyKeyboardMarkup) para facilitar el uso sin recordar comandos:

- **Servidores** — Lista todos los servidores con su estado actual
- **Encender** — Elige un servidor de la lista para encenderlo
- **Estado** — Consulta el estado de un servidor específico
- **Servidor** (admin) — Submenú con Info, Añadir, Eliminar
- **Usuario** (admin) — Submenú con Listar, Añadir, Eliminar

---

## Roles

| Rol   | Comandos disponibles                                                          |
| ----- | ----------------------------------------------------------------------------- |
| admin | Todos los comandos y todo el menú interactivo                                |
| user  | `/start`, `/servers`, `/status`, `/on`, `/version` y menú reducido |

---

## Licencia

GNU General Public License v3.0. Ver [LICENSE](LICENSE).
