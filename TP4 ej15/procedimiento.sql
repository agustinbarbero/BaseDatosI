DELIMITER //
CREATE PROCEDURE AuditarAccesos()
BEGIN
    -- Declaracion de variables
    DECLARE usuario_id INT;
    DECLARE fecha_acceso DATETIME;
    DECLARE direccion_ip VARCHAR(45);
    DECLARE intentos_fallidos INT;
    DECLARE estado_acceso VARCHAR(20);
    DECLARE fecha_actual DATETIME;
    DECLARE fin_cursor BOOLEAN DEFAULT FALSE;

    -- Declarar el cursor con los últimos 100 registros
    DECLARE cursor_accesos CURSOR FOR
        SELECT UsuarioId, FechaAcceso, DireccionIP
        FROM Accesos
        ORDER BY FechaAcceso DESC
        LIMIT 100;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET fin_cursor = TRUE;
    
    START TRANSACTION;
    
    BEGIN
        OPEN cursor_accesos;
        SET fecha_actual = NOW();

        -- Recorrer los registros del cursor
        WHILE NOT fin_cursor DO
            FETCH cursor_accesos INTO usuario_id, fecha_acceso, direccion_ip;

            -- Verificar si llegamos al final del cursor
            IF fin_cursor THEN
                LEAVE;
            END IF;

            -- Contar los intentos fallidos desde la misma IP en las últimas 24 horas
            SELECT COUNT(*) INTO intentos_fallidos
            FROM AuditoriaAccesos
            WHERE DireccionIP = direccion_ip
              AND FechaAcceso >= DATE_SUB(fecha_actual, INTERVAL 24 HOUR)
              AND FechaAcceso < fecha_actual
              AND EstadoAcceso = 'Fallido';

            -- Determinar el estado de acceso
            IF intentos_fallidos >= 3 THEN
                SET estado_acceso = 'Fallido';
            ELSE
                SET estado_acceso = 'Exitoso';
            END IF;

            INSERT INTO AuditoriaAccesos (UsuarioId, FechaAcceso, DireccionIP, EstadoAcceso)
            VALUES (usuario_id, fecha_acceso, direccion_ip, estado_acceso);
        END WHILE;

        -- Cerrar el cursor
        CLOSE cursor_accesos;

        -- Si todo fue exitoso, confirmar la transacción
        COMMIT TRANSACTION;
    END
    BEGIN CATCH
        -- Manejo de errores: si ocurre un error, deshacemos la transacción
        ROLLBACK;
    END CATCH;
END//
DELIMITER ;