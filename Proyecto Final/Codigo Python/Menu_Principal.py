# Importamos los CRUD de cada entidad
from CRUD_Productos import menu_productos
from CRUD_Clientes import menu_clientes
from CRUD_Ordenes import menu_ordenes

def menu_principal():
    while True:
        print("\n--- Sistema de Gestión de Ventas ---")
        print("1. Gestión de Productos")
        print("2. Gestión de Clientes")
        print("3. Gestión de Órdenes")
        print("4. Salir del sistema")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                menu_productos()
            case "2":
                menu_clientes()
            case "3":
                menu_ordenes()
            case "4":
                print("Gracias por usar el sistema. ¡Hasta luego!")
                break
            case _:
                print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu_principal()
