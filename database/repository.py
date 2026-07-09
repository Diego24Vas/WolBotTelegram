from database.db import get_connection, execute_db


def registrar_usuario(user_id: int, username: str | None = None, rol: str = "user"):
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO usuarios (id, username, rol) VALUES (?, ?, ?)",
        (user_id, username, rol),
    )
    conn.commit()


async def registrar_usuario_async(user_id: int, username: str | None = None, rol: str = "user"):
    return await execute_db(registrar_usuario, user_id, username, rol)


def obtener_usuario(user_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


async def obtener_usuario_async(user_id: int):
    return await execute_db(obtener_usuario, user_id)


def actualizar_rol_usuario(user_id: int, rol: str):
    conn = get_connection()
    conn.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (rol, user_id))
    conn.commit()


async def actualizar_rol_usuario_async(user_id: int, rol: str):
    return await execute_db(actualizar_rol_usuario, user_id, rol)


def eliminar_usuario(user_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM logs WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()


async def eliminar_usuario_async(user_id: int):
    return await execute_db(eliminar_usuario, user_id)


def listar_usuarios():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM usuarios ORDER BY id").fetchall()
    return [dict(r) for r in rows]


async def listar_usuarios_async():
    return await execute_db(listar_usuarios)


def existe_admin():
    conn = get_connection()
    row = conn.execute("SELECT 1 FROM usuarios WHERE rol = 'admin' LIMIT 1").fetchone()
    return row is not None


async def existe_admin_async():
    return await execute_db(existe_admin)


def agregar_servidor(nombre: str, mac: str, ip: str, puerto: int = 9):
    conn = get_connection()
    conn.execute(
        "INSERT INTO servidores (nombre, mac, ip, puerto) VALUES (?, ?, ?, ?)",
        (nombre, mac, ip, puerto),
    )
    conn.commit()


async def agregar_servidor_async(nombre: str, mac: str, ip: str, puerto: int = 9):
    return await execute_db(agregar_servidor, nombre, mac, ip, puerto)


def eliminar_servidor(nombre: str):
    conn = get_connection()
    conn.execute("DELETE FROM servidores WHERE nombre = ?", (nombre,))
    conn.commit()


async def eliminar_servidor_async(nombre: str):
    return await execute_db(eliminar_servidor, nombre)


def obtener_servidor(nombre: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM servidores WHERE nombre = ?", (nombre,)).fetchone()
    return dict(row) if row else None


async def obtener_servidor_async(nombre: str):
    return await execute_db(obtener_servidor, nombre)


def listar_servidores():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM servidores ORDER BY nombre").fetchall()
    return [dict(r) for r in rows]


async def listar_servidores_async():
    return await execute_db(listar_servidores)


def registrar_log(user_id: int, accion: str, detalle: str | None = None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO logs (user_id, accion, detalle) VALUES (?, ?, ?)",
        (user_id, accion, detalle),
    )
    conn.commit()


async def registrar_log_async(user_id: int, accion: str, detalle: str | None = None):
    return await execute_db(registrar_log, user_id, accion, detalle)
