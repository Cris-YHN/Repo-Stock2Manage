import sqlite3

DB_PATH = "database/s2m.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE proveedores DROP COLUMN provincia;")
    print("Columna provincia eliminada correctamente.")
    cursor.execute("ALTER TABLE proveedores DROP COLUMN localidad;")
    print("Columna localidad eliminada correctamente.")
except sqlite3.OperationalError as e:
    print("Ya existe o hubo un error:", e)

conn.commit()
conn.close()