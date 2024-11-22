import sqlite3
from datetime import datetime
from database import conectar

def obtener_input(mensaje, tipo=str):
    """Obtiene y valida un input del usuario."""
    while True:
        try:
            valor = tipo(input(mensaje))
            if tipo == int and valor <= 0:
                raise ValueError("El número debe ser positivo.")
            return valor
        except ValueError:
            print(f"Por favor, ingresa un valor válido ({tipo.__name__}).")

def input_mayuscula(mensaje):
    """Solicita una entrada al usuario y la convierte a mayúsculas."""
    return input(mensaje).strip().upper()

def crear_cliente_y_tienda():
    conn = conectar()
    cursor = conn.cursor()
    
    # Datos del cliente
    nombre_cliente = input_mayuscula("Ingrese el nombre del cliente: ")
    telefono_cliente = input_mayuscula("Ingrese el teléfono del cliente: ")
    
    # Registrar cliente
    cursor.execute("INSERT INTO clientes (nombre, telefono) VALUES (?, ?)", 
                   (nombre_cliente, telefono_cliente))
    cliente_id = cursor.lastrowid
    
    # Datos de la tienda
    nombre_tienda = input_mayuscula("Ingrese el nombre de la tienda: ")
    direccion_tienda = input_mayuscula("Ingrese la dirección de la tienda: ")
    telefono_tienda = input_mayuscula("Ingrese el teléfono de la tienda: ")
    
    # Registrar tienda
    cursor.execute("INSERT INTO tiendas (cliente_id, nombre, direccion, telefono) VALUES (?, ?, ?, ?)",
                   (cliente_id, nombre_tienda, direccion_tienda, telefono_tienda))
    
    conn.commit()
    print("Cliente y tienda registrados con éxito.")
    conn.close()

def ver_clientes_y_tiendas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT clientes.id, clientes.nombre, clientes.telefono, tiendas.nombre, tiendas.direccion, tiendas.telefono
        FROM clientes
        JOIN tiendas ON clientes.id = tiendas.cliente_id
    ''')
    clientes = cursor.fetchall()
    if clientes:
        for cliente in clientes:
            print(f"Cliente ID: {cliente[0]}, Nombre: {cliente[1]}, Teléfono: {cliente[2]}")
            print(f"Tienda: {cliente[3]}, Dirección: {cliente[4]}, Teléfono de la tienda: {cliente[5]}\n")
    else:
        print("No hay clientes y tiendas registradas.")
    conn.close()

def crear_producto():
    conn = conectar()
    cursor = conn.cursor()
    nombre = input_mayuscula("Ingrese el nombre del producto: ")
    codigo = input_mayuscula("Ingrese el código del producto: ")
    precio = obtener_input("Ingrese el precio del producto: ", float)
    
    try:
        cursor.execute("INSERT INTO productos (nombre, codigo, precio) VALUES (?, ?, ?)", 
                       (nombre, codigo, precio))
        conn.commit()
        print("Producto registrado con éxito.")
    except sqlite3.IntegrityError:
        print("Error: El código del producto ya existe.")
    finally:
        conn.close()

def ver_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    if productos:
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Código: {producto[2]}, Precio: {producto[3]}")
    else:
        print("No hay productos registrados.")
    conn.close()

def obtener_productos():
    """Devuelve una lista de productos disponibles en la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

def registrar_venta():
    """Permite registrar múltiples productos en una sola transacción."""
    conn = conectar()
    cursor = conn.cursor()
    
    cliente_id = int(input("Ingrese el ID del cliente: "))
    tienda_id = int(input("Ingrese el ID de la tienda: "))
    
    # Obtener la lista de productos disponibles
    productos = obtener_productos()
    
    if not productos:
        print("No hay productos disponibles para la venta.")
        return

    carrito = []
    while True:
        print("\n--- Lista de Productos ---")
        for producto in productos:
            print(f"ID: {producto[0]}, Producto: {producto[1]}, Precio: ${producto[2]:.2f}")
        
        producto_id = int(input("\nSeleccione el ID del producto (0 para finalizar): "))
        if producto_id == 0:
            break
        
        # Verificar si el producto existe
        producto = next((p for p in productos if p[0] == producto_id), None)
        if not producto:
            print("Producto no encontrado, por favor intente nuevamente.")
            continue
        
        cantidad = int(input(f"Ingrese la cantidad para '{producto[1]}': "))
        if cantidad <= 0:
            print("La cantidad debe ser mayor a 0.")
            continue
        
        # Añadir producto al carrito
        precio_total = producto[2] * cantidad
        carrito.append({
            "producto_id": producto_id,
            "nombre": producto[1],
            "cantidad": cantidad,
            "precio_total": precio_total
        })
        
        print(f"Producto '{producto[1]}' añadido al carrito.\n")
    
    if not carrito:
        print("No se registraron productos. Venta cancelada.")
        return

    # Confirmar la venta
    print("\n--- Resumen de la Venta ---")
    total_general = 0
    for item in carrito:
        print(f"Producto: {item['nombre']}, Cantidad: {item['cantidad']}, Total: ${item['precio_total']:.2f}")
        total_general += item['precio_total']
    print(f"\nTotal de la venta: ${total_general:.2f}")

    confirmar = input("¿Desea confirmar la venta? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Venta cancelada.")
        return

    # Registrar todas las ventas en la base de datos
    fecha = datetime.now().strftime('%Y-%m-%d')
    for item in carrito:
        cursor.execute('''
            INSERT INTO ventas (producto_id, cantidad, fecha, precio_total, tienda_id, cliente_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (item['producto_id'], item['cantidad'], fecha, item['precio_total'], tienda_id, cliente_id))
    
    conn.commit()
    print("Venta registrada con éxito.")
    conn.close()

def ver_total_ventas():
    """Muestra el total de las ventas registradas."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(precio_total) FROM ventas')
    total_ventas = cursor.fetchone()[0] or 0
    print(f"El total de todas las ventas es: ${total_ventas:.2f}")
    conn.close()

def ver_ventas_por_marca():
    """Muestra la cantidad de productos vendidos por cada marca."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT productos.nombre, SUM(ventas.cantidad) AS total_vendido
        FROM ventas
        JOIN productos ON ventas.producto_id = productos.id
        GROUP BY productos.nombre
    ''')
    ventas = cursor.fetchall()
    if ventas:
        for producto, total in ventas:
            print(f"Producto: {producto}, Total Vendido: {total}")
    else:
        print("No hay ventas registradas.")
    conn.close()

def ver_ventas_por_fecha():
    """Filtra las ventas entre un rango de fechas proporcionado por el usuario."""
    conn = conectar()
    cursor = conn.cursor()
    
    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
    
    cursor.execute('''
        SELECT productos.nombre, ventas.cantidad, ventas.fecha, ventas.precio_total
        FROM ventas
        JOIN productos ON ventas.producto_id = productos.id
        WHERE ventas.fecha BETWEEN ? AND ?
        ORDER BY ventas.fecha
    ''', (fecha_inicio, fecha_fin))
    
    ventas = cursor.fetchall()
    if ventas:
        for producto, cantidad, fecha, total in ventas:
            print(f"Producto: {producto}, Cantidad: {cantidad}, Fecha: {fecha}, Total: ${total:.2f}")
    else:
        print("No hay ventas en el rango de fechas seleccionado.")
    conn.close()

def ver_ventas_por_cliente():
    """Filtra las ventas realizadas a un cliente específico."""
    conn = conectar()
    cursor = conn.cursor()
    
    cliente_id = int(input("Ingrese el ID del cliente: "))
    
    cursor.execute('''
        SELECT productos.nombre, ventas.cantidad, ventas.fecha, ventas.precio_total
        FROM ventas
        JOIN productos ON ventas.producto_id = productos.id
        WHERE ventas.cliente_id = ?
        ORDER BY ventas.fecha
    ''', (cliente_id,))
    
    ventas = cursor.fetchall()
    if ventas:
        for producto, cantidad, fecha, total in ventas:
            print(f"Producto: {producto}, Cantidad: {cantidad}, Fecha: {fecha}, Total: ${total:.2f}")
    else:
        print("No hay ventas registradas para este cliente.")
    conn.close()
