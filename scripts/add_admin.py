import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database.db import init_db
from database.repository import registrar_usuario, actualizar_rol_usuario, obtener_usuario


def main():
    user_id_input = input("Telegram user ID: ").strip()
    if not user_id_input.isdigit():
        print("Error: debe ser un número.")
        return

    user_id = int(user_id_input)
    username = input("Username (opcional): ").strip() or None

    init_db()

    user = obtener_usuario(user_id)
    if user:
        actualizar_rol_usuario(user_id, "admin")
        print(f"Usuario {user_id} actualizado a admin.")
    else:
        registrar_usuario(user_id, username, "admin")
        print(f"Usuario {user_id} registrado como admin.")


if __name__ == "__main__":
    main()
