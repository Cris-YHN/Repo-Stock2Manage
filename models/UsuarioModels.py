import sqlite3
from entities.UsuarioEntity import Usuario

DB_PATH = "database/s2m.db"

class UsuarioModel:
    @staticmethod
    def insertar(usuario: Usuario):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO usuarios (nombre, apellido, contrasenia, puesto, activo) VALUES (?, ?, ?, ?, ?)""", (usuario.nombre, usuario.apellido, usuario.contrasenia, usuario.puesto, usuario.activo))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_por_id(id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(*row)
        return None