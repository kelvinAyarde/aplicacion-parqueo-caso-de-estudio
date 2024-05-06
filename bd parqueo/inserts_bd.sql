
-- rol
INSERT INTO rol (id, nombre, descripcion) VALUES
(1, 'Administrador', 'Rol con acceso total al sistema.'),
(2, 'Encargado', 'Rol con permisos de Encargado.');

-- personal
INSERT INTO personal (nombres, apellido_p, apellido_m, nro_ci, telefono, direccion, estado) 
VALUES 
('Juan', 'González', 'Pérez', '1112223', '555-1234', 'Calle Principal #123', 'A'),
('María', 'López', 'Martínez', '2223334', '555-5678', 'Avenida Central #456', 'A'),
('Carlos', 'Sánchez', 'García', '4445556', '555-9012', 'Plaza Mayor #789', 'A'),
('Ana', 'Martínez', 'Rodríguez', '6667778', '555-3456', 'Calle Secundaria #234', 'A'),
('Pedro', 'Hernández', 'Gómez', '8889990', '555-6789', 'Paseo de la Fuente #567', 'A');

INSERT INTO encargado (id, observacion, estado)
VALUES 
(2, 'Encargado numero 1', 'A'),
(3, 'Encargado numero 2', 'A'),
(4, 'Encargado numero 3', 'A'),
(5, 'Encargado numero 4', 'A');

-- usuario
INSERT INTO usuario (usuario, password, estado, id_personal, id_rol) 
VALUES 
('admin1', md5('1234'), 'A', 1, 1),
('encargado1', md5('1234'), 'A', 2, 2),
('encargado2', md5('1234'), 'A', 3, 2),
('encargado3', md5('1234'), 'A', 4, 2),
('encargado4', md5('1234'), 'A', 5, 2);

INSERT INTO modelo_marca (modelo, marca) VALUES
('Corolla', 'Toyota'),
('Camry', 'Toyota'),
('Prius', 'Toyota'),
('Rav4', 'Toyota'),
('Highlander', 'Toyota'),
('Mustang', 'Ford'),
('Fiesta', 'Ford'),
('Focus', 'Ford'),
('Explorer', 'Ford'),
('F-150', 'Ford'),
('Civic', 'Honda'),
('Accord', 'Honda'),
('Fit', 'Honda'),
('HR-V', 'Honda'),
('Pilot', 'Honda');

INSERT INTO servicio_abonado (nombre, precio, descripcion, estado) VALUES 
('Abonado_normal',200, 'puede entrar y salir cuando quieran. Se le asignara el espacio disponible más cercano a partir del 2do piso hasta el 5to.', 'A'),
('Abonado_VIP',400, 'puede entrar y salir cuando quieran. Se les asignara el espacio disponible más cercano en el 1er piso.', 'A');


INSERT INTO servicio_visitante (nombre,precio, descripcion, estado) 
VALUES ('Visitante',5, 'se les cobra 5bs si es que ocupa el estacionamiento hasta 1 hora. Y se les asignara el espacio disponible más cercano a partir del 2do piso hasta el 5to.', 'A');


INSERT INTO piso (id, sigla_piso, descripcion) VALUES 
(1, 'piso1', 'piso exclusivo para Abonados VIP'),
(2, 'piso2', 'piso para visitantes y Abonados'),
(3, 'piso3', 'piso para visitantes y Abonados'),
(4, 'piso4', 'piso para visitantes y Abonados'),
(5, 'piso5', 'piso para visitantes y Abonados');

INSERT INTO lugar (nro_lugar, descripcion, estado, id_piso) VALUES 
('A1', 'Descripción del Lugar A1', 'D', 1),
('A2', 'Descripción del Lugar A2', 'D', 1),
('A3', 'Descripción del Lugar A3', 'D', 1),
('B1', 'Descripción del Lugar B1', 'D', 2),
('B2', 'Descripción del Lugar B2', 'D', 2),
('B3', 'Descripción del Lugar B3', 'D', 2),
('C1', 'Descripción del Lugar C1', 'D', 3),
('C2', 'Descripción del Lugar C2', 'D', 3),
('C3', 'Descripción del Lugar C3', 'D', 3),
('D1', 'Descripción del Lugar D1', 'D', 4),
('D2', 'Descripción del Lugar D2', 'D', 4),
('D3', 'Descripción del Lugar D3', 'D', 4),
('E1', 'Descripción del Lugar E1', 'D', 5),
('E2', 'Descripción del Lugar E2', 'D', 5),
('E3', 'Descripción del Lugar E3', 'D', 5);

/*=========================== NUEVOS DATOS ===========================*/

INSERT INTO vehiculo (placa, color, id_modelo_marca) VALUES 
('ABC123', 'Rojo', 1),
('DEF456', 'Azul', 2),
('GHI789', 'Verde', 3),
('JKL012', 'Blanco', 7),
('MNO345', 'Negro', 2);


INSERT INTO cliente (nombres, apellido_p, apellido_m, nro_ci, email, telefono, direccion, estado_contrato) VALUES 
('Juan', 'Perez', 'Garcia', '1234567', 'juan@example.com', '123456789', 'Calle 123, Ciudad', 'A'),
('Maria', 'Gomez', 'Lopez', '1112223', 'maria@example.com', '987654321', 'Avenida Principal, Pueblo', 'A'),
('Pedro', 'Rodriguez', 'Gavilia', '2223334', 'pedro@example.com', '567890123', 'Carrera 456, Villa', 'A');


INSERT INTO vehiculo_cliente (estado, id_vehiculo, id_cliente) VALUES 
('A', 1, 1), 
('A', 2, 2), 
('A', 3, 3);

INSERT INTO contrato (fecha_inicio, fecha_fin, estado, fecha_registro, id_servicio_abonado, id_cliente) VALUES 
(NOW(), DATE_ADD(NOW(), INTERVAL 1 MONTH), 'A', NOW(), 1, 1),
(NOW(), DATE_ADD(NOW(), INTERVAL 1 MONTH), 'A', NOW(), 1, 2),
(NOW(), DATE_ADD(NOW(), INTERVAL 1 MONTH), 'A', NOW(), 2, 3);


INSERT INTO pago_contrato (monto, observacion, fecha_registro, estado, id_contrato) VALUES 
(200.00, 'prueba 1', NOW(), 'R', 1), 
(200.00, 'prueba 2', NOW(), 'R', 2), 
(400.00, 'prueba 3', NOW(), 'R', 3);









