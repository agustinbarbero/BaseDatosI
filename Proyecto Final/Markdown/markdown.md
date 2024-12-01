# Justificación del Diseño del Sistema de Ventas en Línea

## *Introducción*
El sistema de ventas en línea tiene como objetivo gestionar de manera eficiente los *productos, los **clientes* y las *órdenes de compra*. La base de datos diseñada asegura la integridad y consistencia de los datos, cumple con las mejores prácticas de normalización (1NF, 2NF, 3NF) y es capaz de soportar operaciones críticas como inserciones, actualizaciones y consultas avanzadas.

## *Entidades y Relaciones*
### *Entidades Principales*
1. *Clientes*:
   - Representa a los usuarios que realizan compras en el sistema.
   - *Atributos*:
     - id (clave primaria): Identificador único del cliente.
     - nombre: Nombre completo del cliente.
     - email: Dirección de correo electrónico, debe ser único.
   - Restricciones: 
     - email es único y no puede ser nulo.

2. *Productos*:
   - Representa los bienes disponibles para la venta.
   - *Atributos*:
     - id (clave primaria): Identificador único del producto.
     - nombre: Nombre descriptivo del producto.
     - precio: Precio por unidad del producto.
     - stock: Cantidad disponible en inventario.
   - Restricciones:
     - nombre debe ser único y no nulo.

3. *Órdenes*:
   - Registra las compras realizadas por los clientes.
   - *Atributos*:
     - id (clave primaria): Identificador único de la orden.
     - id_cliente (clave foránea): Cliente que realizó la compra.
     - id_producto (clave foránea): Producto adquirido.
     - cantidad: Cantidad de unidades compradas.
     - total: Total de la orden calculado como cantidad * precio.
     - fecha: Fecha en que se realizó la compra.
   - Restricciones:
     - Relación con Clientes y Productos mediante claves foráneas.

### *Relaciones*
1. *Clientes-Órdenes*: Un cliente puede realizar muchas órdenes, pero una orden pertenece a un único cliente.
   - Cardinalidad: 1:N.
2. *Productos-Órdenes*: Un producto puede estar asociado con muchas órdenes, pero cada orden se asocia con un único producto.
   - Cardinalidad: 1:N.

---

## *Normalización*
### *1NF (Primera Forma Normal)*
- Cada tabla tiene atributos atómicos, sin valores repetidos o multi-valuados.
- Ejemplo: En la tabla Órdenes, id_cliente y id_producto son claves foráneas simples.

### *2NF (Segunda Forma Normal)*
- Todos los atributos no clave son dependientes de la clave primaria completa.
- Ejemplo: nombre y email en la tabla Clientes dependen exclusivamente de id.

### *3NF (Tercera Forma Normal)*
- No existen dependencias transitivas entre atributos.
- Ejemplo: En la tabla Órdenes, total depende directamente de los valores de cantidad y precio de Productos, lo que evita redundancia.

---

## *Restricciones de Integridad*
1. *Claves Primarias y Foráneas*:
   - Cada tabla tiene una clave primaria (id).
   - Órdenes incluye claves foráneas (id_cliente y id_producto) para mantener relaciones consistentes.
2. *Restricciones NOT NULL*:
   - Campos esenciales como nombre, email, precio, y stock no permiten valores nulos.
3. *Restricciones UNIQUE*:
   - El campo email de Clientes y nombre de Productos deben ser únicos.

---



