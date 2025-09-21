import sqlite3
from entities.ProveedorEntity import Proveedor

DB_PATH = "database/s2m.db"

class ProveedorModel:

    @staticmethod
    def insertar(Proveedor: Proveedor):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO proveedores (nombre_proveedor, codigo_postal, calle, numero, telefono) VALUES (?, ?, ?, ?, ?)""", (Proveedor.nombre_proveedor, Proveedor.codigo_postal, Proveedor.calle, Proveedor.numero, Proveedor.telefono))
        conn.commit()
        conn.close()
    
    @staticmethod
    def actualizar_proveedor(id, nombre, cp, calle, numero, telefono):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proveedores 
            SET nombre_proveedor = ?, codigo_postal = ?, calle = ?, numero = ?, telefono = ?
            WHERE id_proveedor = ?
        """, (nombre, cp, calle, numero, telefono,id))
        conn.commit()
        conn.close()
    
    @staticmethod
    def obtener_todos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""SELECT pr.id_proveedor, pr.nombre_proveedor, pr.codigo_postal,
        cp.provincia, cp.ciudad, pr.calle, pr.numero, pr.telefono
        FROM proveedores pr LEFT JOIN codigos_postales cp ON pr.codigo_postal = cp.codigo_postal
        """)
        rows = cursor.fetchall()
        conn.close()
        return [Proveedor(*row) for row in rows]
    
    @staticmethod
    def obtener_por_ID(id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""SELECT pr.id_proveedor, pr.nombre_proveedor, pr.codigo_postal,
        cp.provincia, cp.ciudad, pr.calle, pr.numero, pr.telefono
        FROM proveedores pr LEFT JOIN codigos_postales cp ON pr.codigo_postal = cp.codigo_postal 
        WHERE id_proveedor = ?""", (id,))
        rows = cursor.fetchall()
        conn.close()
        return [Proveedor(*row) for row in rows]