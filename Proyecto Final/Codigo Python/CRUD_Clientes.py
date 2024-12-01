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

def agregar_cliente(nombre, email, telefono, direccion):
    sql = "INSERT INTO Clientes (nombre, email, telefono, direccion) VALUES (%s, %s, %s, %s)"
    valores = (nombre, email, telefono, direccion)
    cursor.execute(sql, valores)
    conexion.commit()
    print("Usuario agregado exitosamente.")

def mostrar_cliente_porId(id):
    while not id.isdigit() or int(id) < 0:  
        print("Error, el ID del cliente debe ser un número entero positivo.")
        id = input("Ingrese nuevamente el ID del cliente: ")

    sql = f"SELECT * FROM Clientes WHERE id={id}"
    cursor.execute(sql)
    datos = cursor.fetchall()
    encontrado = False
    for registro in datos:
        print(registro)
        if registro[0] == int(id):
            encontrado = True 
    
    if not encontrado:
        print("Cliente no encontrado")
    return encontrado

def mostrar_lista_clientes():
    sql = f"SELECT * FROM Clientes"
    cursor.execute(sql)
    datos = cursor.fetchall()
    for registro in datos:
        print(registro)

def mostrar_clientes_con_ordenes_superiores_a_un_monto(monto_minimo):
    sql = '''
        SELECT 
            Clientes.id, Clientes.nombre, SUM(Ordenes.total) AS ingresos_totales
        FROM 
            Clientes
        INNER JOIN 
            Ordenes ON Clientes.id = Ordenes.id_cliente
        GROUP BY 
            Clientes.id, Clientes.nombre
        HAVING 
            ingresos_totales > %s
        ORDER BY 
            ingresos_totales DESC
    '''
    cursor.execute(sql, (monto_minimo,))
    resultados = cursor.fetchall()
    for cliente in resultados:
        print(f"ID: {cliente[0]}, Nombre: {cliente[1]}, Ingresos Totales: ${cliente[2]:.2f}")

def modificar_cliente(id,nombre,direccion,telefono,email):
    sql = "UPDATE Clientes SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE id=%s"
    valores = (nombre, direccion, telefono, email, id)
    cursor.execute(sql, valores)
    conexion.commit()
    print("Usuario modificado exitosamente.")

def eliminar_cliente(id):
    #"""sql = f"DELETE FROM Clientes WHERE id={id}"
    #cursor.execute(sql)
    #conexion.commit()"""
    
    try:
        # Verificar si el cliente tiene órdenes asociadas
        sql_verificar_ordenes = "SELECT id FROM Ordenes WHERE id_cliente = %s"
        cursor.execute(sql_verificar_ordenes, (id,))
        ordenes_asociadas = cursor.fetchall()

        if ordenes_asociadas:
            print(f"El cliente con ID {id} tiene {len(ordenes_asociadas)} órdenes asociadas.")
            confirmacion = input("¿Desea eliminar las órdenes asociadas antes de eliminar al cliente? (S/s para confirmar): ").lower()

            if confirmacion == 's':
                # Eliminar las órdenes asociadas
                sql_eliminar_ordenes = "DELETE FROM Ordenes WHERE id_cliente = %s"
                cursor.execute(sql_eliminar_ordenes, (id,))
                print(f"Órdenes asociadas eliminadas.")

            else:
                print("Operación cancelada. No se eliminó el cliente.")
                return

        # Eliminar el cliente
        sql_eliminar_cliente = "DELETE FROM Clientes WHERE id = %s"
        cursor.execute(sql_eliminar_cliente, (id,))

        # Confirmar la transacción
        conexion.commit()
        print(f"Cliente con ID {id} eliminado exitosamente.")

    except mysql.connector.Error as error:
        # Revertir la transacción si ocurre un error
        conexion.rollback()
        print(f"Error al eliminar el cliente: {error}")
    except Exception as e:
        conexion.rollback()
        print(f"Error general: {e}")


# Interfaz de usuario (CLI)
def menu_clientes():
    while True:
        print("\n Gestión de Clientes")
        print("1. Agregar Cliente")
        print("2. Ver Cliente por ID")
        print("3. Mostrar todos los Clientes")
        print("4. Mostrar Clientes con ordenes superiores a un monto")
        print("5. Actualizar Cliente")
        print("6. Borrar Cliente")
        print("7. Salir del Menú de Clientes")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case '1':
                nombre = input("Nombre: ")
                while nombre.isspace() or nombre.isdigit() or not nombre.isalpha():  
                    print("Error, el nombre debe ser una cadena de caracteres.")
                    nombre = input("Nombre: ")

                email = input("Email: ")
                while not email.count('@') == 1 or email.count('.') == 0:
                    print("Error, el email debe tener un formato válido.")
                    email = input("Email: ")
                    
                telefono = input("Teléfono: ")
                while not telefono.isdigit() or len(telefono) > 15:
                    print("Error, el teléfono debe tener un formato válido y no debe superar los 15 caracteres.")
                    telefono = input("Teléfono: ")

                direccion = input("Dirección: ")
                while direccion.isspace() or len(direccion) < 5 or len(direccion) > 50:
                    print("Error, la dirección no puede estar vacía.")
                    direccion = input("Dirección: ") 

                agregar_cliente(nombre, email, telefono, direccion)
            case '2':
                id = input("ID del cliente: ")
                mostrar_cliente_porId(id)

            case '3':
                mostrar_lista_clientes()

            case '4':
                monto=input("Ingrese un monto minimo para buscar todos los clientes que tengan una orden mayor a ese numero: ")
                while not monto.isdigit() or float(monto) == 0:  
                    print("Error, el monto debe ser un número positivo.")
                    monto = input("Monto: ")
                mostrar_clientes_con_ordenes_superiores_a_un_monto(monto)
                
            case '5':
                id = input("ID del cliente: ")
                if mostrar_cliente_porId(id):
                    nombre = input("Nombre: ")
                    while nombre.isspace() or nombre.isdigit() or not nombre.isalpha():  
                        print("Error, el nombre debe ser una cadena de caracteres.")
                        nombre = input("Nombre: ")

                    email = input("Email: ")
                    while not email.count('@') == 1 or email.count('.') == 0:
                        print("Error, el email debe tener un formato válido.")
                        email = input("Email: ")
                        
                    telefono = input("Teléfono: ")
                    while not telefono.isdigit() or len(telefono) > 15:
                        print("Error, el teléfono debe tener un formato válido y no debe superar los 15 caracteres.")
                        telefono = input("Teléfono: ")

                    direccion = input("Dirección: ")
                    while direccion.isspace() or len(direccion) < 5 or len(direccion) > 50:
                        print("Error, la dirección no puede estar vacía.")
                        direccion = input("Dirección: ") 
                        
                    modificar_cliente(id, nombre, email, direccion, telefono)
                    
            case '6':
                id = input("ID del cliente: ")
                if mostrar_cliente_porId(id):
                    seguro = input("Confirme con S/s para eliminar o N/n para rechazar: ")
                    while seguro.lower() != 's' and seguro.lower() != 'n':
                        print("Error, se ingreso algo distinto de S/s o N/n.")
                        seguro = input("Ingrese nuevamente S/s para eliminar o N/n para rechazar: ")
                    if seguro.lower()=='s':
                        eliminar_cliente(id)
                    else:
                        print("No se elimino el cliente")
                        
            case '7':
                print("Saliendo del menú de clientes")
                break
            case _:
                print("Opción inválida, intente nuevamente.")