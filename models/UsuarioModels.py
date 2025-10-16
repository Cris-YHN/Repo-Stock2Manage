import sqlite3
import bcrypt
import secrets
import smtplib
from email.mime.text import MIMEText
from entities.UsuarioEntity import Usuario
from datetime import datetime, date

DB_PATH = "database/s2m.db"

class UsuarioModel:
    @staticmethod
    def insertar(usuario: Usuario):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO usuarios (nombre, apellido, contrasenia, email, puesto, activo) VALUES (?, ?, ?, ?, ?, ?)""", (usuario.nombre, usuario.apellido, usuario.contrasenia, usuario.email, usuario.puesto, usuario.activo))
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
    def actualizar_usuario(id_usuario, nombre, apellido, email, puesto):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios 
            SET nombre = ?, apellido = ?, email = ?, puesto = ?
            WHERE id_usuario = ?
        """, (nombre, apellido, email, puesto, id_usuario))
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
            SELECT id_usuario, nombre, apellido, contrasenia, email, puesto, activo
            FROM usuarios
            WHERE apellido LIKE ?
        """, (f"%{apellido}%",))
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(*row) for row in rows]
    
    @staticmethod
    def generar_codigo_hash(id_usuario):
        codigo = secrets.token_hex(4).upper()  # Ejemplo: 'A1F3C9D4'
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET codigohash = ? WHERE id_usuario = ?", (codigo, id_usuario))
        conn.commit()
        conn.close()
        return codigo

    @staticmethod
    def enviar_codigo_email(email, codigo):
        remitente = "stock2manage.v1@gmail.com"  # 🔥 CAMBIAR por tu correo
        password = "xcmv atgd qpyl nbfy"

        msg = MIMEText(f"Tu código de recuperación de contraseña es: {codigo}")
        msg["Subject"] = "Recuperación de contraseña"
        msg["From"] = remitente
        msg["To"] = email

        try:
            # Gmail usa SSL directo por puerto 465
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(remitente, password)
                server.send_message(msg)
            print(f"✅ Correo enviado a {email}")
        except smtplib.SMTPAuthenticationError:
            print("❌ Error de autenticación: revisá el correo o la contraseña de aplicación.")
            raise
        except Exception as e:
            print(f"❌ Error al enviar correo: {e}")
            raise

    @staticmethod
    def actualizar_contrasenia(id_usuario, nueva_contrasenia):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET contrasenia = ?, codigohash = NULL WHERE id_usuario = ?", (nueva_contrasenia, id_usuario))
        conn.commit()
        conn.close()
    
    @staticmethod
    def registrar_intento_fallido(id_usuario):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        hoy = date.today().isoformat()

        # Obtener datos actuales
        cursor.execute("SELECT intentos_fallidos, fecha_ultimo_intento FROM usuarios WHERE id_usuario = ?", (id_usuario,))
        row = cursor.fetchone()

        intentos = 0
        fecha = None
        if row:
            intentos, fecha = row

        # Si es un nuevo día, reiniciamos el contador
        if fecha != hoy:
            intentos = 0

        intentos += 1

        # Guardar intento actualizado
        cursor.execute("""
            UPDATE usuarios
            SET intentos_fallidos = ?, fecha_ultimo_intento = ?
            WHERE id_usuario = ?
        """, (intentos, hoy, id_usuario))

        # Si superó el límite, bloquear
        if intentos >= 5:
            cursor.execute("UPDATE usuarios SET activo = 0 WHERE id_usuario = ?", (id_usuario,))
            print(f"🚫 Usuario {id_usuario} bloqueado por 5 intentos fallidos hoy")

        conn.commit()
        conn.close()

    @staticmethod
    def resetear_intentos(id_usuario):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios 
            SET intentos_fallidos = 0, fecha_ultimo_intento = NULL
            WHERE id_usuario = ?
        """, (id_usuario,))
        conn.commit()
        conn.close()
