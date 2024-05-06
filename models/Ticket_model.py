from database.db import conectar_bd
from .entidades.Ticket_ent import Ticket
from utils.formato_time import fecha_hora,fecha_hora_javascript

class Ticket_modelo():

    @classmethod
    def registrar_ticket(cls, ticket,cliente,reg_pago):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor: 
                cursor.execute('call RegistrarTicket(%s,%s,%s,%s,%s)', 
                               (ticket.id_lugar,ticket.id_vehiculo,ticket.id_encargado,cliente,reg_pago))
                resultado = cursor.fetchone()
                if resultado[0] == 'Exito':
                    datos_consulta = [True,resultado[1]]
                else:
                    datos_consulta = [False,resultado[1]]
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            return [False,ex]

    @classmethod
    def buscar_vehiculo_placa_ticket(cls, placa):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute('call buscar_vehiculo_placa_ticket(%s)', (placa,))
                resultado = cursor.fetchone()
                datos_consulta = [False,'algo salio mal']
                if resultado:
                    if resultado[0] == 'Error':
                        datos_consulta = [False,resultado[1]]
                    else:
                        dato = {
                            'id_vehiculo': resultado[0],
                            'placa': resultado[1],
                            'modelo_marca': resultado[2],
                            'color': resultado[3],
                            'tipo_cliente': resultado[4]
                        }
                        if len(resultado) > 5:
                            dato['id_cliente'] = resultado[5]
                            dato['cliente_nombres'] = resultado[6]
                            dato['cliente_apellido'] = resultado[7]
                            if len(resultado) > 8:
                                dato['existe_vehiculo_tiket'] = 'S' if resultado[8] == 1 else 'N' #si el resultado es 1 entonces es S de lo contratio N
                        datos_consulta = [True, dato]
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            return [False,ex]

    @classmethod    
    def traer_lugares(cls):    
        try:
            conn = conectar_bd()
            datos_consulta = []
            with conn.cursor() as cursor:
                cursor.execute("""SELECT l.id, l.nro_lugar, p.sigla_piso,l.estado,p.descripcion as piso_descripcion, 
                               l.descripcion as lugar_descripcion
                FROM lugar l JOIN piso p ON p.id = l.id_piso WHERE l.estado = 'D' or l.estado = 'O';""")
                resultado = cursor.fetchall()
                for fila in resultado:
                    dato = {
                        'id': fila[0],
                        'nro_lugar': fila[1],
                        'sigla_piso': fila[2],
                        'estado': fila[3],
                        'piso_descripcion': fila[4],
                        'lugar_descripcion': fila[5]
                    }
                    datos_consulta.append(dato)
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            
    @classmethod
    def buscar_ticket(cls, id_ticket):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT t.id AS id_ticket,t.hora_ingreso as hora_ingreso,
                    CASE
                       WHEN ptv.id IS NULL THEN 'N'
                       WHEN ptv.estado = 'P' THEN 'S'
                       ELSE 'El ticket ya fue pagado, seleccione otro'
                   END AS pagar
                FROM ticket t
                LEFT JOIN pago_ticket_visitante ptv ON t.id = ptv.id_ticket
                WHERE t.id = %s;""", (id_ticket,))
                resultado = cursor.fetchone()
                datos_consulta = [False, 'No existe el Ticket!']
                if resultado:
                    if resultado[2] != 'S' and resultado[2] != 'N' :
                        return [False, resultado[2]]
                    else:
                        dato = {
                            'id_ticket': resultado[0],
                            'hora_ingreso': fecha_hora_javascript(resultado[1]),#formato para recibir en js
                            'pagar': resultado[2]
                        }
                        datos_consulta= [True, dato]
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            return [False, ex]
            
    @classmethod    
    def traer_servicio_visitante(cls):    
        try:
            conn = conectar_bd()
            datos_consulta = []
            with conn.cursor() as cursor:
                cursor.execute("""SELECT sv.id, sv.nombre, sv.precio FROM servicio_visitante sv WHERE sv.estado = 'A';""")
                resultado = cursor.fetchall()
                for fila in resultado:
                    dato = {
                        'id': fila[0],
                        'nombre': fila[1],
                        'precio': fila[2]
                    }
                    datos_consulta.append(dato)
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            
            
    @classmethod
    def registro_pago_ticket(cls,observacion,monto,id_servicio_visitante,id_ticket,abonado):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                if abonado == 'Si':
                    cursor.execute("""UPDATE ticket 
                                    SET hora_salida = NOW(), estado = 'I' 
                                    WHERE id = %s;""", (id_ticket,))
                else:
                    cursor.execute("""UPDATE ticket 
                                    SET hora_salida = NOW(), estado = 'I' 
                                    WHERE id = %s;""", (id_ticket,))
                    cursor.execute("""UPDATE pago_ticket_visitante
                                    SET monto = %s, observacion = %s, fecha_registro = NOW(), id_servicio_visitante = %s
                                    WHERE id_ticket = %s;""", 
                                (monto, observacion, id_servicio_visitante, id_ticket))
            conn.commit()
            conn.close()
            return [True, 'Registro Exitoso!']
        except Exception as ex:
            print(ex)
            return [False,ex]