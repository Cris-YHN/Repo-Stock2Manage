import sqlite3
conn = sqlite3.connect("database/s2m.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE usuarios ADD COLUMN intentos_fallidos INTEGER DEFAULT 0")
cursor.execute("ALTER TABLE usuarios ADD COLUMN fecha_ultimo_intento TEXT")

conn.commit()
conn.close()
print("Migración completada ✅")
