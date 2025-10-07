import sqlite3
from entities.ManufacturaEntity import Manufactura, ManufacturaDetalle

DB_PATH = "database/s2m.db"

class ManufacturaModel:

    @staticmethod
    def insertar(Manufactura: Manufactura):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO manufactura (nombre)
            VALUES (?)
        """, (Manufactura.nombre,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def obtener_manufacturas():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM manufactura")
        rows = cursor.fetchall()
        conn.close()
        return [Manufactura(*row) for row in rows]
    
    @staticmethod
    def obtener_pasos(idmanu):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT man.id_manufactura,
                man.id_paso,
                man.id_material,
                mat.nombre,
                man.cantidad_necesaria
            FROM manufactura_detalles man
            LEFT JOIN materiales mat ON man.id_material = mat.id_material
            WHERE man.id_manufactura = ?
            ORDER BY man.id_paso
        """, (idmanu,))
        rows = cursor.fetchall()
        conn.close()
        return [ManufacturaDetalle(*row) for row in rows]
    
    @staticmethod
    def obtener_por_nombre(nombre):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_manufactura, nombre FROM manufactura
            WHERE nombre LIKE ?
        """, (f"%{nombre}%",))
        rows = cursor.fetchall()
        conn.close()
        return [Manufactura(*row) for row in rows]
    
    @staticmethod
    def actualizar_manufactura(nombre,idmanu):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE manufactura 
            SET nombre = ?
            WHERE id_manufactura = ?
        """, (nombre, idmanu,))
        conn.commit()
        conn.close()
    
    @staticmethod
    def insertar_paso(detalle: ManufacturaDetalle):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO manufactura_detalles (id_manufactura, id_paso, id_material, cantidad_necesaria)
            VALUES (?, ?, ?, ?)
        """, (detalle.id_manufactura, detalle.id_paso, detalle.id_material, detalle.cantidad_necesaria))
        conn.commit()
        conn.close()

    @staticmethod
    def modificar_paso(detalle: ManufacturaDetalle, mat_original: int):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE manufactura_detalles
            SET id_material = ?, cantidad_necesaria = ?
            WHERE id_manufactura = ? AND id_paso = ? AND id_material = ?
        """, (
            detalle.id_material,
            detalle.cantidad_necesaria,
            detalle.id_manufactura,
            detalle.id_paso,
            mat_original     # 👈 usamos el material original
        ))
        conn.commit()
        conn.close()

