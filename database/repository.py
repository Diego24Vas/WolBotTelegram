import asyncio
from database.db import get_connection

def registrar_usuario(user_id: int, username: str | None = None, rol: str = "user"):
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO usuarios (id, username, rol) VALUES (?, ?, ?)",
        (user_id, username, rol),
    )
    conn.commit()
    conn.close()

async def registrar_usuario_async(user_id: int, username: str | None = None, rol: str = "user"):
    return await asyncio.to_thread(registrar_usuario, user_id, username, rol)

def obtener_usuario(user_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

async def obtener_usuario_async(user_id: int):
    return await asyncio.to_thread(obtener_usuario, user_id)

def actualizar_rol_usuario(user_id: int, rol: str):
    conn = get_connection()
    conn.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (rol, user_id))
    conn.commit()
    conn.close()

async def actualizar_rol_usuario_async(user_id: int, rol: str):
    return await asyncio.to_thread(actualizar_rol_usuario, user_id, rol)

def eliminar_usuario(user_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM logs WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

async def eliminar_usuario_async(user_id: int):
    return await asyncio.to_thread(eliminar_usuario, user_id)

def listar_usuarios():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM usuarios ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

async def listar_usuarios_async():
    return await asyncio.to_thread(listar_usuarios)

def existe_admin():
    conn = get_connection()
    row = conn.execute("SELECT 1 FROM usuarios WHERE rol = 'admin' LIMIT 1").fetchone()
    conn.close()
    return row is not None

async def existe_admin_async():
    return await asyncio.to_thread(existe_admin)

def agregar_servidor(nombre: str, mac: str, ip: str, puerto: int = 9):
    conn = get_connection()
    conn.execute(
        "INSERT INTO servidores (nombre, mac, ip, puerto) VALUES (?, ?, ?, ?)",
        (nombre, mac, ip, puerto),
    )
    conn.commit()
    conn.close()

async def agregar_servidor_async(nombre: str, mac: str, ip: str, puerto: int = 9):
    return await asyncio.to_thread(agregar_servidor, nombre, mac, ip, puerto)

def eliminar_servidor(nombre: str):
    conn = get_connection()
    conn.execute("DELETE FROM servidores WHERE nombre = ?", (nombre,))
    conn.commit()
    conn.close()

async def eliminar_servidor_async(nombre: str):
    return await asyncio.to_thread(eliminar_servidor, nombre)

def obtener_servidor(nombre: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM servidores WHERE nombre = ?", (nombre,)).fetchone()
    conn.close()
    return dict(row) if row else None

async def obtener_servidor_async(nombre: str):
    return await asyncio.to_thread(obtener_servidor, nombre)

def listar_servidores():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM servidores ORDER BY nombre").fetchall()
    conn.close()
    return [dict(r) for r in rows]

async def listar_servidores_async():
    return await asyncio.to_thread(listar_servidores)

def registrar_log(user_id: int, accion: str, detalle: str | None = None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO logs (user_id, accion, detalle) VALUES (?, ?, ?)",
        (user_id, accion, detalle),
    )
    conn.commit()
    conn.close()

async def registrar_log_async(user_id: int, accion: str, detalle: str | None = None):
    return await asyncio.to_thread(registrar_log, user_id, accion, detalle)
