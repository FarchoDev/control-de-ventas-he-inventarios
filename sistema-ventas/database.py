import sqlite3

def conectar():
    """Establece una conexión con la base de datos."""
    return sqlite3.connect('promotor.db')

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()
    
    # Tabla de clientes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT
        )
    ''')
    
    # Tabla de tiendas vinculada al cliente
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tiendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            nombre TEXT,
            direccion TEXT,
            telefono TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id) ON DELETE CASCADE
        )
    ''')
    
    # Tabla de productos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            codigo TEXT UNIQUE,
            precio REAL CHECK(precio > 0)
        )
    ''')
    
    # Tabla de ventas vinculada al cliente y la tienda
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            producto_id INTEGER,
            cantidad INTEGER CHECK(cantidad > 0),
            fecha TEXT,
            precio_total REAL,
            tienda_id INTEGER,
            cliente_id INTEGER,
            FOREIGN KEY (producto_id) REFERENCES productos (id),
            FOREIGN KEY (tienda_id) REFERENCES tiendas (id),
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    ''')
    
    conn.commit()
    conn.close()

crear_tablas()
