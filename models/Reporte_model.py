from database.db import conectar_bd
from utils.formato_time import fecha_hora,fecha_hora_javascript,fecha

class Reporte_modelo():
    
    @classmethod
    def reporte_vehiculo_estacionamiento(cls):
        try:
            conn = conectar_bd()
            datos_consulta = []
            with conn.cursor() as cursor:
                cursor.execute("""SELECT t.id, p.sigla_piso, l.nro_lugar , v.placa, 
                    CASE
                    WHEN ptv.id IS NULL THEN 'Abonado'
                    ELSE 'Visitante'
                    END AS tipo_cliente,
                t.hora_ingreso,t.estado
                FROM ticket t JOIN lugar l ON l.id = t.id_lugar
                JOIN piso p ON p.id = l.id_piso
                JOIN vehiculo v ON v.id = t.id_vehiculo
                LEFT JOIN pago_ticket_visitante ptv ON ptv.id_ticket = t.id
                ORDER BY t.hora_ingreso DESC;""")
                resultado = cursor.fetchall()
                for fila in resultado:
                    estado = 'Estacionado' if fila[6] == 'A' else 'Retirado'
                    dato = {
                        'id_ticket': fila[0],
                        'piso': fila[1],
                        'lugar': fila[2],
                        'placa': fila[3],
                        'tipo_cliente': fila[4],
                        'fecha_hora_ingreso': fecha_hora(fila[5]),
                        'estado': estado
                    }
                    datos_consulta.append(dato)
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
    
    @classmethod
    def reporte_salida_vehiculo(cls):
        try:
            conn = conectar_bd()
            datos_consulta = []
            with conn.cursor() as cursor:
                cursor.execute("""SELECT t.id, p.sigla_piso, l.nro_lugar , v.placa, 
                    CASE
                    WHEN ptv.id IS NULL THEN 'Abonado'
                    ELSE 'Visitante'
                    END AS tipo_cliente,
                t.hora_ingreso,t.hora_salida,
                TIMESTAMPDIFF(HOUR, t.hora_ingreso, t.hora_salida) AS horas_transcurridas,
    			TIMESTAMPDIFF(MINUTE, t.hora_ingreso, t.hora_salida) % 60 AS minutos_transcurridos
                FROM ticket t JOIN lugar l ON l.id = t.id_lugar
                JOIN piso p ON p.id = l.id_piso
                JOIN vehiculo v ON v.id = t.id_vehiculo
                LEFT JOIN pago_ticket_visitante ptv ON ptv.id_ticket = t.id
                WHERE t.estado = 'I'
                ORDER BY t.hora_salida DESC;""")
                resultado = cursor.fetchall()
                for fila in resultado:
                    tiempo = str(fila[7]) + ' Horas y ' + str(fila[8])  +' Minutos'
                    dato = {
                        'id_ticket': fila[0],
                        'piso': fila[1],
                        'lugar': fila[2],
                        'placa': fila[3],
                        'tipo_cliente': fila[4],
                        'fecha_hora_ingreso': fecha_hora(fila[5]),
                        'fecha_hora_salida': fecha_hora(fila[6]),
                        'tiempo_transcurrido': tiempo
                    }
                    datos_consulta.append(dato)
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            
    @classmethod
    def reporte_contrato_vigente(cls):
        try:
            conn = conectar_bd()
            datos_consulta = []
            with conn.cursor() as cursor:
                cursor.execute("""SELECT CONCAT(c.nombres,' ',c.apellido_p,' ',c.apellido_m) as nombre_cliente, COUNT(vc.id_cliente) as cantidad_vehiculos,
                    sa.nombre as servicio_abonado,co.fecha_inicio as contrato_fecha_inicio ,co.fecha_fin as contrato_fecha_fin,co.id
                FROM cliente c JOIN vehiculo_cliente vc ON vc.id_cliente = c.id 
                JOIN contrato co ON co.id_cliente = c.id
                JOIN servicio_abonado sa ON sa.id = co.id_servicio_abonado
                WHERE vc.estado='A' AND co.estado = 'A'
                GROUP by co.id
                ORDER BY co.id DESC;""")
                resultado = cursor.fetchall()
                for fila in resultado:
                    dato = {
                        'nombre_cliente': fila[0],
                        'cantidad_vehiculos': fila[1],
                        'servicio_abonado': fila[2],
                        'contrato_fecha_inicio': fecha(fila[3]),
                        'contrato_fecha_fin': fecha(fila[4])
                    }
                    datos_consulta.append(dato)
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
