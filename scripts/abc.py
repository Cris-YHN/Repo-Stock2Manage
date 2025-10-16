import sqlite3

conn = sqlite3.connect("database/s2m.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM codigos_postales;")
conn.commit()
conn.close()

print("✅ Todos los códigos postales fueron eliminados.")