# from conexion import conexion, cursor
import mysql.connector

conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="045123",   # capaz es la otra
    database="ventas"
)

cursor = conexion.cursor()   # Creacion del cursor
# Comprobar si se conecto la base de datos:
if conexion.is_connected():
    print("Conexión exitosa")
else:
    print("No se pudo conectar")

def agregar_producto(nombre,precio,stock):
    sql = 'INSERT INTO Productos (nombre, precio, stock) VALUES (%s, %s, %s)'
    valores = (nombre, precio, stock)
    cursor.execute(sql, valores)
    conexion.commit()
    print("Producto agregado.")

def mostrar_producto_porId(id):
    while not id.isdigit() or int(id) < 0:  
        print("Error, el ID del producto debe ser un número entero positivo.")
        id = input("Ingrese nuevamente el ID del producto: ")

    sql = f"SELECT * FROM Productos WHERE id={id}"
    cursor.execute(sql)
    datos = cursor.fetchall()
    encontrado = False
    for registro in datos:
        print(registro)
        if registro[0] == int(id):
            encontrado = True 
    
    if not encontrado:
        print("Producto no encontrado")
    return encontrado

def mostrar_todos_los_productos():
    cursor.execute("SELECT * FROM Productos")
    datos = cursor.fetchall()
    for registro in datos:
        print(registro)


def modificar_producto(id, nombre,precio,stock):
    while not id.isdigit() or int(id) < 0:  
        print("Error, el ID debe ser un número entero positivo.")
        id = input("Ingrese nuevamente el ID: ")

    sql = 'UPDATE Productos SET nombre=%s, precio = %s, stock = %s WHERE id = %s'
    valores = (nombre, precio, stock, id)
    cursor.execute(sql, valores)
    conexion.commit()
    print("Producto modificado")

def eliminar_producto(id):
    sql = f'DELETE FROM Productos WHERE id = {id}'
    cursor.execute(sql)
    conexion.commit()
    print("Producto eliminado")


# Interfaz de usuario (CLI)
def menu_productos():
    while True:
        print("\n Gestion de Productos")
        print("1. Agregar Producto")
        print("2. Ver Producto por ID")
        print("3. Mostrar todos los productos")
        print("4. Modificar Producto")
        print("5. Borrar Producto")
        print("6. Salir del Menu de Productos")
        opcion = input("Seleccione una opcion: ")
        
        match opcion:
            case '1':
                nombre = input("Nombre: ")
                while nombre.isspace() or nombre.isdigit() or not nombre.isalpha():  
                    print("Error, el nombre debe ser una cadena de caracteres.")
                    nombre = input("Nombre: ")

                precio = input("Precio: ")
                while not precio.isdigit() or float(precio) == 0:  
                    print("Error, el precio debe ser un número positivo.")
                    precio = input("Precio: ")

                stock = input("Stock: ")
                while not stock.isdigit() or int(stock) < 0:  
                    print("Error, el stock debe ser un número entero positivo.")
                    stock = input("Stock: ")
                agregar_producto(nombre, precio, stock)

            case '2':
                id = input("id del producto: ")
                mostrar_producto_porId(id)

            case '3':
                mostrar_todos_los_productos()

            case '4':
                id = input("id del producto: ")
                if mostrar_producto_porId(id):
                    nombre = input("Nombre: ")
                    while nombre.isspace() or nombre.isdigit() or not nombre.isalpha():  
                        print("Error, el nombre debe ser una cadena de caracteres.")
                        nombre = input("Nombre: ")

                    precio = input("Precio: ")
                    while not precio.isdigit() or float(precio) == 0:  
                        print("Error, el precio debe ser un número positivo.")
                        precio = input("Precio: ")

                    stock = input("Stock: ")
                    while not stock.isdigit() or int(stock) < 0:  
                        print("Error, el stock debe ser un número entero positivo.")
                        stock = input("Stock: ")
                    modificar_producto(id, nombre, precio, stock)

            case '5':
                id = input("id del producto: ")
                if mostrar_producto_porId(id):
                    seguro = input("Confirme con S/s para eliminar o N/n para rechazar: ")
                    while seguro.lower() != 's' and seguro.lower() != 'n':
                        print("Error, se ingreso algo distinto de S/s o N/n.")
                        seguro = input("Ingrese nuevamente S/s para eliminar o N/n para rechazar: ")
                    if seguro.lower()=='s':
                        eliminar_producto(id)
                    else:
                        print("No se elimino el producto")
                
            case '6':
                print("Sale del menu de productos")
                break
            case _:
                print("Opción inválida, intente nuevamente.")

        


