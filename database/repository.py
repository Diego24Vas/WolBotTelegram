from database.db import get_connection

def registrar_usuario(user_id: int, username: str | None = None, rol: str = "user"):
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO usuarios (id, username, rol) VALUES (?, ?, ?)",
        (user_id, username, rol),
    )
    conn.commit()
    conn.close()

def obtener_usuario(user_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def actualizar_rol_usuario(user_id: int, rol: str):
    conn = get_connection()
    conn.execute("UPDATE usuarios SET rol = ? WHERE id = ?", (rol, user_id))
    conn.commit()
    conn.close()

def eliminar_usuario(user_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM logs WHERE user_id = ?", (user_id,))
    conn.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def listar_usuarios():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM usuarios ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def existe_admin():
    conn = get_connection()
    row = conn.execute("SELECT 1 FROM usuarios WHERE rol = 'admin' LIMIT 1").fetchone()
    conn.close()
    return row is not None

def agregar_servidor(nombre: str, mac: str, ip: str, puerto: int = 9):
    conn = get_connection()
    conn.execute(
        "INSERT INTO servidores (nombre, mac, ip, puerto) VALUES (?, ?, ?, ?)",
        (nombre, mac, ip, puerto),
    )
    conn.commit()
    conn.close()

def eliminar_servidor(nombre: str):
    conn = get_connection()
    conn.execute("DELETE FROM servidores WHERE nombre = ?", (nombre,))
    conn.commit()
    conn.close()

def obtener_servidor(nombre: str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM servidores WHERE nombre = ?", (nombre,)).fetchone()
    conn.close()
    return dict(row) if row else None

def listar_servidores():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM servidores ORDER BY nombre").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def registrar_log(user_id: int, accion: str, detalle: str | None = None):
    conn = get_connection()
    conn.execute(
        "INSERT INTO logs (user_id, accion, detalle) VALUES (?, ?, ?)",
        (user_id, accion, detalle),
    )
    conn.commit()
    conn.close()
