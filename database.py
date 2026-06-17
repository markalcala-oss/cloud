import sqlite3

def get_connection():
    # Esto creará un archivo llamado 'local_leads.db' en la raíz de tu proyecto
    conn = sqlite3.connect("local_leads.db")
    conn.row_factory = sqlite3.Row  # Permite que Flask lea los datos como diccionarios
    return conn

def init_db():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_completo TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefono TEXT NOT NULL,
            interes_servicio TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        connection.commit()
    finally:
        connection.close()

def insert_lead(nombre, email, telefono, servicio):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        sql = """
        INSERT INTO leads (nombre_completo, email, telefono, interes_servicio)
        VALUES (?, ?, ?, ?);
        """
        cursor.execute(sql, (nombre, email, telefono, servicio))
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Si el correo está repetido
    finally:
        connection.close()

def get_all_leads():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM leads ORDER BY fecha_registro DESC;")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()