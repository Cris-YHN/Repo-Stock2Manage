import sqlite3
import bcrypt
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
    
    @staticmethod
    def obtener_todos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(*row) for row in rows]
    
    @staticmethod
    def obtener_activos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE activo = 1")
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(*row) for row in rows]


    @staticmethod
    def obtener_solicitudes():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE activo = 0")
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(*row) for row in rows]
    
    @staticmethod
    def obtener_busqueda_por_id(id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = ?", (id,))
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(*row) for row in rows]

    @staticmethod
    def cambiar_estado_usuario(id_usuario, activo):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET activo = ? WHERE id_usuario = ?", (activo, id_usuario))
        conn.commit()
        conn.close()

    @staticmethod
    def actualizar_usuario(id_usuario, nombre, apellido, puesto):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios 
            SET nombre = ?, apellido = ?, puesto = ?
            WHERE id_usuario = ?
        """, (nombre, apellido, puesto, id_usuario))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar_usuario(id_usuario):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_inactivos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE activo = 2")
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(*row) for row in rows]
    
    @staticmethod
    def hash_password(password: str) -> str:
        # Genera el hash con salt
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")  # se guarda como texto en la DB
    
    @staticmethod
    def check_password(password: str, hashed: str) -> bool:
        # Verifica la contraseña ingresada contra el hash almacenado
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    
    @staticmethod
    def buscar_por_apellido(apellido: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_usuario, nombre, apellido, contrasenia, puesto, activo
            FROM usuarios
            WHERE apellido LIKE ?
        """, (f"%{apellido}%",))
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(*row) for row in rows]
