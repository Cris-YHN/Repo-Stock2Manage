import sqlite3
from entities.MaterialEntity import Material

DB_PATH = "database/s2m.db"

class MaterialModel:

    @staticmethod
    def insertar(material: Material):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO materiales (nombre, stock_disponible, id_proveedor, activo, max_ingreso)
            VALUES (?, ?, ?, ?, ?)
        """, (material.nombre, material.stock_disponible, material.id_proveedor,
              material.activo, material.max_ingreso))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_activos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        SELECT m.id_material, m.nombre, m.stock_disponible, m.id_proveedor, p.nombre_proveedor, m.max_ingreso, m.activo
        FROM materiales m
        LEFT JOIN proveedores p ON m.id_proveedor = p.id_proveedor
        WHERE m.activo = 1""")
        rows = cursor.fetchall()
        conn.close()
        return [Material(*row) for row in rows]

    @staticmethod
    def obtener_inactivos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id_material, m.nombre, m.stock_disponible, m.id_proveedor, p.nombre_proveedor, m.max_ingreso, m.activo
            FROM materiales m
            LEFT JOIN proveedores p ON m.id_proveedor = p.id_proveedor
            WHERE m.activo = 0
        """)
        rows = cursor.fetchall()
        conn.close()
        return [Material(*row) for row in rows]

    @staticmethod
    def obtener_escasos():
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id_material, m.nombre, m.stock_disponible, m.id_proveedor, p.nombre_proveedor, m.max_ingreso, m.activo
            FROM materiales m
            LEFT JOIN proveedores p ON m.id_proveedor = p.id_proveedor
            WHERE m.stock_disponible < (m.max_ingreso * 0.5)
              AND m.activo = 1
        """)
        rows = cursor.fetchall()
        conn.close()
        return [Material(*row) for row in rows]

    @staticmethod
    def obtener_por_id(id_material):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.id_material, m.nombre, m.stock_disponible, m.id_proveedor, p.nombre_proveedor, m.max_ingreso, m.activo
            FROM materiales m
            LEFT JOIN proveedores p ON m.id_proveedor = p.id_proveedor
            WHERE m.id_material = ?
        """, (id_material,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Material(*row)
        return None

    @staticmethod
    def actualizar(id_material, nombre, stock, id_proveedor):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE materiales
            SET nombre = ?, stock_disponible = ?, id_proveedor = ?
            WHERE id_material = ?
        """, (nombre, stock, id_proveedor, id_material))
        conn.commit()
        conn.close()

    @staticmethod
    def cambiar_estado(id_material, activo):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE materiales SET activo = ? WHERE id_material = ?", (activo, id_material))
        conn.commit()
        conn.close()

    @staticmethod
    def cargar_remito(id_material, cantidad):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE materiales
            SET stock_disponible = stock_disponible + ?,
                max_ingreso = CASE
                    WHEN ? > max_ingreso THEN ?
                    ELSE max_ingreso
                END
            WHERE id_material = ?
        """, (cantidad, cantidad, cantidad, id_material))
        conn.commit()
        conn.close()
    
    @staticmethod
    def material_existe(id_material):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM materiales WHERE id_material = ?", (id_material,))
        found = cursor.fetchone() is not None
        conn.close()
        return found
    
    @staticmethod
    def descontar_material(cantidad, id_material):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Verificar stock disponible
        cursor.execute("SELECT stock_disponible FROM materiales WHERE id_material = ?", (id_material,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise ValueError("El material no existe.")
        if row[0] < cantidad:
            conn.close()
            raise ValueError("Stock insuficiente para realizar el proceso.")

        # Descontar stock
        cursor.execute("""
            UPDATE materiales
            SET stock_disponible = stock_disponible - ?
            WHERE id_material = ?
        """, (cantidad, id_material))
        conn.commit()
        conn.close()