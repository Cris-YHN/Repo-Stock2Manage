import sqlite3
conn = sqlite3.connect("database/s2m.db")
cur = conn.cursor()
cur.execute("PRAGMA table_info(USUARIOS)")
for row in cur.fetchall():
    print(row)
conn.close()

