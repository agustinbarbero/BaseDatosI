# from conexion import conexion, cursor
import mysql.connector
from CRUD_Clientes import mostrar_cliente_porId
from CRUD_Productos import mostrar_producto_porId
conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="045123",   # capaz es la otra
    database="ventas"
)

cursor = conexion.cursor()  # Creación del cursor

if conexion.is_connected():
    print("Conexión exitosa a la base de datos")
else:
    print("No se pudo conectar a la base de datos")


def agregar_orden(id_cliente, id_producto, cantidad, fecha):
    sql_precio = "SELECT stock, precio FROM Productos WHERE id = %s"
    cursor.execute(sql_precio,(id_producto,))
    resultado = cursor.fetchone()
    if not resultado:
        print("Producto no encontrado")
        return
    stock_actual=resultado[0] 
    precio = resultado[1]
    if cantidad > stock_actual:
        print(f"Stock insuficiente. Disponible: {stock_actual}, solicitado: {cantidad}")
        return
    
    total = cantidad * precio
    
    sql = '''
        INSERT INTO Ordenes (id_cliente, id_producto, cantidad, total, fecha)
        VALUES (%s, %s, %s, %s, %s)
    '''
    valores = (id_cliente, id_producto, cantidad, total, fecha)
    cursor.execute(sql,valores)

    # Actualizar el stock del producto
    nuevo_stock = stock_actual - cantidad
    sql_actualizar_stock = "UPDATE Productos SET stock = %s WHERE id = %s"
    cursor.execute(sql_actualizar_stock, (nuevo_stock, id_producto))
    
    conexion.commit()
    print("Orden agregada y stock actualizado.")


def mostrar_orden_por_id(id):
    while not id.isdigit() or int(id) < 0:  
        print("Error, el ID de la orden debe ser un número entero positivo.")
        id = input("Ingrese nuevamente el ID de la orden: ")

    sql = f"SELECT * FROM Ordenes WHERE id={id}"
    cursor.execute(sql)
    datos = cursor.fetchall()
    encontrado = False
    for registro in datos:
        print(registro)
        if registro[0] == int(id):
            encontrado = True 
    
    if not encontrado:
        print("Orden no encontrada")
    return encontrado


def mostrar_todas_las_ordenes():
    cursor.execute("SELECT * FROM Ordenes")
    datos = cursor.fetchall()
    for registro in datos:
        print(registro)

def mostrar_ordenes_con_detalles_de_Clientes_Productos():
    sql=""" 
    SELECT 
    o.id AS id_orden,
    c.nombre AS cliente,
    p.nombre AS producto,
    o.cantidad,
    o.total,
    o.fecha
    FROM 
    Ordenes o
    INNER JOIN 
    Clientes c ON o.id_cliente = c.id
    INNER JOIN 
    Productos p ON o.id_producto = p.id
    ORDER BY 
        o.fecha DESC;

    """
    cursor.execute(sql)
    datos=cursor.fetchall()
    for orden in datos:
        print(f"ID Orden: {orden[0]}, Cliente: {orden[1]}, Producto: {orden[2]}, "
              f"Cantidad: {orden[3]}, Total: ${orden[4]:.2f}, Fecha: {orden[5]}")

def modificar_orden(id, id_cliente, id_producto, cantidad, fecha):
    sql_precio = "SELECT precio FROM Productos WHERE id = %s"
    cursor.execute(sql_precio,(id_producto,))
    resultado = cursor.fetchone()
    if not resultado:
        print("Producto no encontrado")
        return
    
    precio = resultado[0]
    total = cantidad * precio

    sql = '''
        UPDATE Ordenes SET id_cliente=%s, id_producto=%s, cantidad=%s, total=%s, fecha=%s
        WHERE id=%s
    '''
    valores = (id_cliente, id_producto, cantidad, total, fecha, id)
    cursor.execute(sql, valores)
    conexion.commit()
    print("Orden modificada.")


def eliminar_orden(id):
    sql = f'DELETE FROM Ordenes WHERE id={id}'
    cursor.execute(sql)
    conexion.commit()
    print("Orden eliminada.")


def menu_ordenes():
    while True:
        print("\n Gestión de Órdenes")
        print("1. Agregar Orden")
        print("2. Ver Orden por ID")
        print("3. Mostrar todas las Órdenes")
        print("4. Mostrar todas las Órdenes con detalles de clientes y productos")
        print("5. Modificar Orden")
        print("6. Borrar Orden")
        print("7. Salir del Menú de Órdenes")
        opcion = input("Seleccione una opción: ")

        match opcion:
            case '1':
                id_cliente = input("ID del cliente: ")
                if not mostrar_cliente_porId(id_cliente):
                    print("Cliente no encontrado.")
                    break
                
                id_producto = input("ID del producto: ")
                if not mostrar_producto_porId(id_producto):
                    print("Producto no encontrado.")
                    break

                # Solicitar cantidad y fecha
                cantidad = int(input("Cantidad: "))
                while cantidad <= 0:
                    print("La cantidad debe ser un número positivo.")
                    cantidad = int(input("Cantidad: "))
                    
                fecha = input("Fecha (YYYY-MM-DD): ")

                agregar_orden(id_cliente, id_producto, cantidad, fecha)

            case '2':
                id = input("ID de la orden: ")
                mostrar_orden_por_id(id)

            case '3':
                mostrar_todas_las_ordenes()

            case '4':
                mostrar_ordenes_con_detalles_de_Clientes_Productos()

            case '5':
                id_orden = input("ID de la orden: ")
                if mostrar_orden_por_id(id_orden):
                    id_cliente = input("Nuevo ID del cliente: ")
                    while not mostrar_cliente_porId(id_cliente):
                        id_cliente = input("Ingrese nuevamente el ID del cliente: ")

                    id_producto = input("Nuevo ID del producto: ")
                    while not mostrar_producto_porId(id_producto):
                        id_producto = input("Ingrese nuevamente el ID del producto: ")
                   
                    # Solicitar cantidad y fecha
                    cantidad = int(input("Nueva Cantidad: "))
                    while cantidad <= 0:
                        print("La cantidad debe ser un número positivo.")
                        cantidad = int(input("Nueva Cantidad: "))
                            
                    fecha = input("Fecha (YYYY-MM-DD): ")
                    modificar_orden(id_orden, id_cliente, id_producto, cantidad, fecha)

            case '6':
                id = input("ID de la orden: ")
                if mostrar_orden_por_id(id):
                    seguro = input("Confirme con S/s para eliminar o N/n para rechazar: ")
                    while seguro.lower() != 's' and seguro.lower() != 'n':
                        print("Error, se ingreso algo distinto de S/s o N/n.")
                        seguro = input("Ingrese nuevamente S/s para eliminar o N/n para rechazar: ")
                    if seguro.lower()=='s':
                        eliminar_orden(id)
                    else:
                        print("No se elimino la orden")
                        
            case '7':
                print("Saliendo del menú de órdenes")
                break
            case _:
                print("Opción inválida, intente nuevamente.")
