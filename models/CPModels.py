import sqlite3
from entities.CPEntity import CodigoPostal

DB_PATH = "database/s2m.db"

class CodePostalModel:
    
    @staticmethod
    def obtener_todos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM codigos_postales")
        rows = cursor.fetchall()
        conn.close()
        return [CodigoPostal(*row) for row in rows]
    
    @staticmethod
    def Obtener_por_nombre(ciudad):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM codigos_postales WHERE ciudad = ?", (f"%{ciudad}%"))
        rows = cursor.fetchall()
        conn.close()
        if rows:
            return [CodigoPostal(*row) for row in rows]
        return None