import sqlite3 as sql
DB_PATH = "database/s2m.db"

def create_table_usuarios():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            contrasenia TEXT NOT NULL,
            puesto TEXT NOT NULL,
            activo INTEGER DEFAULT 0,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            email TEXT NOT NULL,
            codigohash TEXT,
            intentos_fallidos INTEGER DEFAULT 0,
            fecha_ultimo_intento TEXT
        )"""
    )

    # ----- Semilla de autoincrement a 1_000_000 -----
    # Solo si no hay registros y la secuencia aún no está creada
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        # crea la entrada en sqlite_sequence con seq = 999999
        cursor.execute("""
            INSERT OR REPLACE INTO sqlite_sequence (name, seq)
            VALUES ('usuarios', 999999)
        """)
    # -----------------------------------------------

    conn.commit()
    conn.close()

def create_table_codigos_postales():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS codigos_postales (
            codigo_postal TEXT PRIMARY KEY,
            ciudad TEXT NOT NULL,
            provincia TEXT NOT NULL,
            pais TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()

def create_table_proveedores():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS proveedores (
            id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_proveedor TEXT NOT NULL,
            codigo_postal TEXT NOT NULL,
            calle TEXT,
            numero TEXT,
            telefono TEXT,
            FOREIGN KEY (codigo_postal) REFERENCES codigos_postales(codigo_postal)
        )"""
    )
    conn.commit()
    conn.close()

def create_table_materiales():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS materiales (
            id_material INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            stock_disponible INTEGER DEFAULT 0,
            id_proveedor INTEGER NOT NULL,
            activo INTEGER DEFAULT 1,
            max_ingreso INTEGER DEFAULT 0,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
        )"""
    )
    conn.commit()
    conn.close()

def create_table_remitos():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS remitos (
            id_remito INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_remito TEXT NOT NULL,
            id_proveedor INTEGER NOT NULL,
            FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
        )"""
    )
    conn.commit()
    conn.close()

def create_table_remito_detalles():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS remito_detalles (
            id_remito INTEGER,
            id_material INTEGER,
            cantidad INTEGER NOT NULL,
            PRIMARY KEY (id_remito, id_material),
            FOREIGN KEY (id_remito) REFERENCES remitos(id_remito),
            FOREIGN KEY (id_material) REFERENCES materiales(id_material)
        )"""
    )
    conn.commit()
    conn.close()

def create_table_manufactura():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS manufactura (
            id_manufactura INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )"""
    )
    conn.commit()
    conn.close()

def create_table_manufactura_detalles():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS manufactura_detalles (
            id_manufactura INTEGER,
            id_paso INTEGER,
            id_material INTEGER,
            cantidad_necesaria INTEGER NOT NULL,
            PRIMARY KEY (id_manufactura, id_paso, id_material),
            FOREIGN KEY (id_manufactura) REFERENCES manufactura(id_manufactura),
            FOREIGN KEY (id_material) REFERENCES materiales(id_material)
        )"""
    )
    conn.commit()
    conn.close()

def create_table_logs():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT,
                accion TEXT,
                nivel TEXT,
                equipo TEXT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """)
    conn.commit()
    conn.close()

def crear_todas_tablas():
    create_table_usuarios()
    create_table_codigos_postales()
    create_table_proveedores()
    create_table_materiales()
    create_table_remitos()
    create_table_remito_detalles()
    create_table_manufactura()
    create_table_manufactura_detalles()
    create_table_logs()

