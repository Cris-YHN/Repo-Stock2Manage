import sqlite3
from datetime import datetime
from entities.LogsEntity import logs

DB_PATH = "database/s2m.db"

class LogsModel:
    @staticmethod
    def insertar_log(log: logs):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (usuario, accion, nivel, equipo, fecha)
            VALUES (?, ?, ?, ?, ?)
        """, (log.usuario, log.accion, log.nivel, log.equipo, log.fecha or datetime.now()))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_logs():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, usuario, accion, nivel, equipo, fecha FROM logs ORDER BY fecha DESC")
        rows = cursor.fetchall()
        conn.close()
        return [logs(*row) for row in rows]