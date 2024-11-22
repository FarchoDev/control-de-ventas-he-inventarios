from models import *

def menu():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Registrar nuevo cliente y tienda")
        print("2. Ver clientes y tiendas")
        print("3. Añadir nuevo producto")
        print("4. Ver productos")
        print("5. Registrar venta")
        print("6. Ver total de ventas")
        print("7. Ver ventas por producto")
        print("8. Ver ventas por fecha")
        print("9. Ver ventas por cliente")
        print("10. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            crear_cliente_y_tienda()
        elif opcion == '2':
            ver_clientes_y_tiendas()
        elif opcion == '3':
            crear_producto()
        elif opcion == '4':
            ver_productos()
        elif opcion == '5':
            registrar_venta()
        elif opcion == '6':
            ver_total_ventas()
        elif opcion == '7':
            ver_ventas_por_marca()
        elif opcion == '8':
            ver_ventas_por_fecha()
        elif opcion == '9':
            ver_ventas_por_cliente()
        elif opcion == '10':
            print("Saliendo...")
            break
        else:
            print("Opción no válida, intente de nuevo.")

if __name__ == "__main__":
    menu()
