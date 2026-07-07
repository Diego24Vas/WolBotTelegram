CREATE_TABLES = """
CREATE TABLE IF NOT EXISTS usuarios (
    id          INTEGER PRIMARY KEY,
    username    TEXT,
    rol         TEXT NOT NULL DEFAULT 'user',
    creado_en   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS servidores (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL UNIQUE,
    mac         TEXT NOT NULL,
    ip          TEXT NOT NULL,
    puerto      INTEGER NOT NULL DEFAULT 9,
    creado_en   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS logs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    accion      TEXT NOT NULL,
    detalle     TEXT,
    creado_en   TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES usuarios(id)
);
"""
