-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS ventas;
USE ventas;

CREATE TABLE Clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255),
    telefono VARCHAR(15),
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE Ordenes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    fecha DATE NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES Productos(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);


-- Índices para optimizar consultas
CREATE INDEX idx_cliente_orden ON Ordenes(id_cliente);
CREATE INDEX idx_producto_orden ON Ordenes(id_producto);

-- Inserción de datos iniciales en Clientes
INSERT INTO Clientes (nombre, email, telefono, direccion)
VALUES
    ('Juan Pérez', 'juan.perez@example.com', '555-1234', 'Calle Falsa 123'),
    ('María García', 'maria.garcia@example.com', '555-5678', 'Av. Siempre Viva 456'),
    ('Luis López', 'luis.lopez@example.com', '555-9101', 'Boulevard de los Sueños 789'),
    ('Ana Torres', 'ana.torres@example.com', '555-1122', 'Calle Luna 321'),
    ('Carlos Díaz', 'carlos.diaz@example.com', '555-3344', 'Calle Sol 654'),
    ('Laura Martínez', 'laura.martinez@example.com', '555-5566', 'Calle Estrella 987'),
    ('Jorge Gómez', 'jorge.gomez@example.com', '555-7788', 'Av. Universo 123'),
    ('Sofía Herrera', 'sofia.herrera@example.com', '555-9900', 'Calle Cosmos 456'),
    ('Pedro Ramos', 'pedro.ramos@example.com', '555-1010', 'Calle Galaxia 789'),
    ('Mónica Ruiz', 'monica.ruiz@example.com', '555-2020', 'Calle Cometa 321');

-- Inserción de datos iniciales en Productos
INSERT INTO Productos (nombre, precio, stock)
VALUES
    ('Laptop HP', 800.00, 50),
    ('Teclado Mecánico', 100.00, 200),
    ('Mouse Inalámbrico', 25.00, 150),
    ('Monitor LED', 300.00, 80),
    ('Auriculares Bluetooth', 50.00, 100),
    ('Impresora Multifunción', 150.00, 30),
    ('Tablet Android', 250.00, 40),
    ('Disco SSD 1TB', 120.00, 70),
    ('Memoria RAM 16GB', 90.00, 120),
    ('Smartphone', 600.00, 60);

-- Inserción de datos iniciales en Órdenes
INSERT INTO Ordenes (id_cliente, id_producto, cantidad, total, fecha)
VALUES
    (1,clientes 2, 3, 300.00, '2024-11-25'),
    (2, 3, 1, 25.00, '2024-11-20'),
    (3, 1, 5, 4000.00, '2024-11-22'),
    (4, 4, 2, 600.00, '2024-11-23'),
    (5, 5, 4, 200.00, '2024-11-21'),
    (6, 2, 3, 300.00, '2024-11-25'),
    (7, 3, 1, 25.00, '2024-11-24'),
    (8, 1, 2, 1600.00, '2024-11-20'),
    (9, 4, 1, 300.00, '2024-11-22'),
    (10, 5, 2, 100.00, '2024-11-23');

-- Consulta para verificar datos
SELECT * FROM Clientes;
SELECT * FROM Productos;
SELECT * FROM Ordenes;

-- Procedimiento almacenado para consultar órdenes por cliente
DELIMITER $$
CREATE PROCEDURE VerOrdenesPorCliente (IN cliente_id INT)
BEGIN
    SELECT 
        o.id AS OrdenID,
        c.nombre AS Cliente,
        p.nombre AS Producto,
        o.cantidad,
        o.total,
        o.fecha
    FROM Ordenes o
    INNER JOIN Clientes c ON o.id_cliente = c.id
    INNER JOIN Productos p ON o.id_producto = p.id
    WHERE o.id_cliente = cliente_id
    ORDER BY o.fecha DESC;
END $$
DELIMITER ;

