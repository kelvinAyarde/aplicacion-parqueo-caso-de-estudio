
/*------------------------ PROGRAMACION PARQUEO V2 ---------------------------------*/


/*========================== PROCEDIMIENTOS ALMACENADOS ============================*/

-- verificar credenciales de usuario
DELIMITER //
CREATE PROCEDURE verificar_credencial(
    IN p_usuario VARCHAR(50),
    IN p_password VARCHAR(128)
)
BEGIN	
	SELECT p.id as id_personal, r.id as id_rol, p.nombres, p.apellido_p, p.apellido_m,u.usuario as usuario, r.nombre as rol
    FROM personal p
    JOIN usuario u ON p.id = u.id_personal
    JOIN rol r ON u.id_rol = r.id
    WHERE u.usuario = p_usuario AND u.password = md5(p_password)
    AND u.estado = 'A' AND p.estado = 'A';
END //
DELIMITER ;

/*------------------------------------------- NO esta completo -------------------------------*/
-- buscar_vehiculo_placa_ticket para obtener los datos del vehiculo y cliente al registrar un ticket
DELIMITER //
CREATE PROCEDURE buscar_vehiculo_placa_ticket(IN p_placa VARCHAR(10))
BEGIN
    -- Declaración de variables
    DECLARE cliente_tipo VARCHAR(20);
	DECLARE estado_contrato CHAR(1);  
    DECLARE v_placa VARCHAR(10);
    DECLARE v_modelo_marca VARCHAR(30);
    DECLARE v_color VARCHAR(20); 
    -- Variables para control de existencia de vehículo y cliente
    DECLARE existe_vehiculo INT;
    DECLARE vehiculo_id INT;
    DECLARE existe_cliente INT;
    DECLARE cliente_id INT;
	DECLARE existe_vehiculo_ticket INT; -- es para saber si el vehiculo de un cliente ya se encuentra con ticket
    -- Verificar si el vehículo existe
    SELECT COUNT(*), id INTO existe_vehiculo, vehiculo_id 
    FROM vehiculo WHERE placa = p_placa;  
    -- Si el vehículo no existe
    IF existe_vehiculo = 0 THEN
        SELECT 'Error' AS estado, 'No existe un vehiculo con esa placa' AS mensaje;
    ELSE
        -- Verificar si el vehículo tiene un cliente relacionado
        SELECT COUNT(*), vc.id_cliente INTO existe_cliente, cliente_id 
        FROM vehiculo_cliente vc WHERE vc.id_vehiculo = vehiculo_id AND vc.estado = 'A';
		-- Datos de vehiculo, por defecto es visitante
		SET cliente_tipo = 'Visitante';
		SELECT vehiculo_id, v.placa, CONCAT(mm.modelo,' ',mm.marca) AS modelo_marca, v.color, cliente_tipo
		INTO vehiculo_id,v_placa, v_modelo_marca, v_color, cliente_tipo
        FROM vehiculo v JOIN modelo_marca mm ON mm.id = v.id_modelo_marca
        WHERE v.id = vehiculo_id;
     
        IF existe_cliente = 0 THEN
			-- Si el vehículo no tiene cliente relacionado	
            SELECT vehiculo_id,v_placa, v_modelo_marca, v_color, cliente_tipo;
        ELSE
            -- Si el vehículo tiene un cliente relacionado, verificar el estado del contrato
            SELECT c.estado_contrato INTO estado_contrato FROM cliente c WHERE c.id = cliente_id; 

            IF estado_contrato = 'A' THEN
				SELECT COUNT(*) INTO existe_vehiculo_ticket 
				FROM vehiculo_cliente vc JOIN ticket t ON t.id_vehiculo = vc.id_vehiculo
				where vc.id_cliente = cliente_id AND vc.estado = 'A' AND t.estado = 'A';
                -- Si el contrato del cliente está activo, se envia el tipo de cliente que es por contrato y sus datos
                SELECT vehiculo_id,v_placa, v_modelo_marca, v_color, sa.nombre AS tipo_cliente,cliente_id, c.nombres, c.apellido_p,existe_vehiculo_ticket
                FROM cliente c JOIN contrato co ON co.id_cliente = c.id
                JOIN servicio_abonado sa ON sa.id = co.id_servicio_abonado
                WHERE co.estado = 'A' AND c.id = cliente_id;
            ELSE
                -- Si el contrato del cliente no está activo, se considera como visitante
                SELECT vehiculo_id,v_placa, v_modelo_marca, v_color, cliente_tipo,cliente_id, c.nombres, c.apellido_p
                FROM cliente c WHERE c.id = cliente_id;
            END IF;
        END IF;
    END IF;
END //
DELIMITER ;

-- RegistrarTicket
DELIMITER //
CREATE PROCEDURE RegistrarTicket (
    IN p_id_lugar INT,
    IN p_id_vehiculo INT,
    IN p_id_encargado INT,
    IN p_id_cliente INT,
    IN p_reg_pago CHAR(1) -- recibe si se registra un pago S o N, solo los visitantes pagan
)
BEGIN
    DECLARE v_lugar_estado CHAR(1);
    DECLARE v_id_ticket INT;
    DECLARE existe_vehiculo_ticket INT;
    -- Iniciar transacción
    START TRANSACTION;
    -- Verificar si el lugar tiene estado 'O' o 'I'
    SELECT estado INTO v_lugar_estado FROM lugar WHERE id = p_id_lugar;

    IF v_lugar_estado NOT IN ('O', 'I') THEN
        IF p_reg_pago = 'S' THEN
            -- Registro de ticket para visitantes
            INSERT INTO ticket (hora_ingreso, estado, id_lugar, id_vehiculo, id_encargado) 
            VALUES (NOW(), 'A', p_id_lugar, p_id_vehiculo, p_id_encargado);
            SELECT LAST_INSERT_ID() INTO v_id_ticket;
            INSERT INTO pago_ticket_visitante (id_ticket, estado) VALUES (v_id_ticket, 'P');
            COMMIT;
            SELECT 'Exito' AS estado, 'Ticket Visitante registrado exitosamente' AS mensaje;
        ELSE
            -- Verificar si el vehículo del cliente ya tiene un ticket registrado
            SELECT COUNT(*) INTO existe_vehiculo_ticket 
            FROM vehiculo_cliente vc JOIN ticket t ON t.id_vehiculo = vc.id_vehiculo
            WHERE vc.id_cliente = p_id_cliente AND vc.estado = 'A' AND t.estado = 'A';

            IF existe_vehiculo_ticket = 0 THEN 
                -- Registro de ticket para abonados sin ticket previo
                INSERT INTO ticket (hora_ingreso, estado, id_lugar, id_vehiculo, id_encargado) 
                VALUES (NOW(), 'A', p_id_lugar, p_id_vehiculo, p_id_encargado);
                COMMIT;
                SELECT 'Exito' AS estado, 'Ticket Abonado registrado exitosamente' AS mensaje;
            ELSE
                -- Registro de ticket para abonados con ticket previo
                INSERT INTO ticket (hora_ingreso, estado, id_lugar, id_vehiculo, id_encargado) 
                VALUES (NOW(), 'A', p_id_lugar, p_id_vehiculo, p_id_encargado);
                SELECT LAST_INSERT_ID() INTO v_id_ticket;
                INSERT INTO pago_ticket_visitante (id_ticket, estado) VALUES (v_id_ticket, 'P');
                COMMIT;
                SELECT 'Exito' AS estado, 'Ticket Visitante registrado exitosamente' AS mensaje;
            END IF;
        END IF;
    ELSE
        -- Cancelar la transacción si el lugar está ocupado o inactivo
        ROLLBACK;
        SELECT 'Error' AS estado, 'No se puede registrar el ticket, el lugar está ocupado o inactivo' AS mensaje;
    END IF;
END//
DELIMITER ;

-- registrar_contrato
DELIMITER //
CREATE PROCEDURE registrar_contrato(
    IN p_fecha_inicio DATE,
    IN p_id_servicio_abonado INT,
    IN p_id_cliente INT
)
BEGIN
    DECLARE contrato_id INT;
    DECLARE monto_pago NUMERIC(10, 2);
    DECLARE fecha_fin_contrato DATE;
	-- Obtener el precio del servicio abonado
    SELECT precio INTO monto_pago FROM servicio_abonado WHERE id = p_id_servicio_abonado;
	-- Calcular la fecha de fin
	SET fecha_fin_contrato = DATE_ADD(p_fecha_inicio, INTERVAL 1 MONTH);
	-- Registrar el contrato
    INSERT INTO contrato (fecha_inicio, fecha_fin, estado, fecha_registro, id_servicio_abonado, id_cliente)
    VALUES (p_fecha_inicio, fecha_fin_contrato, 'E', NOW(), p_id_servicio_abonado, p_id_cliente);
    -- Obtener el ID del contrato recién insertado
    SET contrato_id = LAST_INSERT_ID();
    -- Crear el pago del contrato
    INSERT INTO pago_contrato (monto, estado, id_contrato) VALUES (monto_pago, 'P', contrato_id);
END //
DELIMITER ;



/*========================== TRIGGERS ============================*/

-- registro_ticket_ocupar_lugar
DELIMITER //
CREATE TRIGGER registro_ticket_ocupar_lugar
AFTER INSERT ON ticket
FOR EACH ROW
BEGIN
    UPDATE lugar
    SET estado = 'O'
    WHERE id = NEW.id_lugar;
END//
DELIMITER ;

-- Actualizar el estado del ticket a 'I' cuando se registra un pago visitante
DELIMITER //
CREATE TRIGGER registro_pago_ticket_visitante
AFTER UPDATE ON pago_ticket_visitante
FOR EACH ROW
BEGIN
	IF NEW.estado = 'R' THEN
		UPDATE ticket
		SET estado = 'I'
		WHERE id = NEW.id_ticket;
	END IF;
END//
DELIMITER ;

-- Actualizar el estado del lugar a 'D' 
DELIMITER //
CREATE TRIGGER actualizar_estado_lugar_disponible
AFTER UPDATE ON ticket
FOR EACH ROW
BEGIN
    IF NEW.estado = 'I' THEN
        UPDATE lugar l
        SET l.estado = 'D'
        WHERE l.id = NEW.id_lugar;
    END IF;
END//
DELIMITER ;

-- actualizar_estado_contrato_al_pagar al hacer una actulizacion en pago_contrato al cambiar de estado
DELIMITER //
CREATE TRIGGER actualizar_estado_contrato_al_pagar
AFTER UPDATE ON pago_contrato
FOR EACH ROW
BEGIN    
    IF NEW.estado = 'R' THEN        
        UPDATE contrato
        SET estado = 'A'
        WHERE id = NEW.id_contrato;
    END IF;
END//
DELIMITER ;

-- actualizar_estado_cliente_abonado
DELIMITER //
CREATE TRIGGER actualizar_estado_cliente
AFTER UPDATE ON contrato
FOR EACH ROW
BEGIN
    UPDATE cliente
    SET estado_contrato = NEW.estado
    WHERE id = NEW.id_cliente;
END //
DELIMITER ;











