import sqlite3
from entities.RemitosEntity import Remito, RemitoDetalle

DB_PATH = "database/s2m.db"

class RemitoModel:

    @staticmethod
    def insertar(remito):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO remitos (fecha_remito, id_proveedor)
            VALUES (?, ?)
        """, (remito.fecha_remito, remito.id_proveedor))
        remito_id = cursor.lastrowid

        # insertar detalles
        for det in remito.detalles:
            cursor.execute("""
                INSERT INTO remito_detalles (id_remito, id_material, cantidad)
                VALUES (?, ?, ?)
            """, (remito_id, det.id_material, det.cantidad))

        conn.commit()
        conn.close()
        return remito_id


    @staticmethod
    def obtener_todos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id_remito, r.fecha_remito, r.id_proveedor, p.nombre_proveedor
            FROM remitos r
            LEFT JOIN proveedores p ON r.id_proveedor = p.id_proveedor
        """)
        rows = cursor.fetchall()
        conn.close()
        return [Remito(*row) for row in rows]

    @staticmethod
    def obtener_remitos_por_fecha(patron_fecha):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Usa LIKE para buscar por año, año-mes o año-mes-día
        cursor.execute("""
            SELECT r.id_remito, r.fecha_remito, r.id_proveedor, p.nombre_proveedor
            FROM remitos r
            LEFT JOIN proveedores p ON r.id_proveedor = p.id_proveedor
            WHERE r.fecha_remito LIKE ?
        """, (f"{patron_fecha}%",))
        rows = cursor.fetchall()
        conn.close()
        return [Remito(*row) for row in rows] if rows else []

    @staticmethod
    def actualizar_proveedor(id_remito, id_proveedor):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE remitos
            SET id_proveedor = ?
            WHERE id_remito = ?
        """, (id_proveedor, id_remito))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_detalles_por_remito(id_remito):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT rd.id_remito, rd.id_material, m.nombre, rd.cantidad
            FROM remito_detalles rd
            LEFT JOIN materiales m ON rd.id_material = m.id_material
            WHERE id_remito = ?
        """, (id_remito,))
        rows = cursor.fetchall()
        conn.close()
        return [RemitoDetalle(*row) for row in rows]