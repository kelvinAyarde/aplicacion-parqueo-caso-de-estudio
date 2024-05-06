from database.db import conectar_bd
from .entidades.Cliente_ent import Cliente
from .entidades.Contrato_ent import ServicioAbonado
#utils
from utils.formato_time import fecha,fecha_hora

class Contrato_modelo():

    @classmethod
    def registrar_contrato(cls, contrato):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute('call registrar_contrato(%s, %s, %s)', (contrato.fecha_inicio, 
                contrato.id_servicio_abonado,contrato.id_cliente))
                conn.commit()
            conn.close()
            return [True,'Registro Exitoso!']
        except Exception as ex:
            print(ex)
            return [False,ex]

    @classmethod
    def registrar_abonado(cls, abonado):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO cliente_abonado (id, email, telefono, direccion, estado_contrato)
                VALUES (%s, %s, %s, %s, %s);""", (abonado.id,abonado.email,abonado.telefono,
                                                  abonado.direccion,abonado.estado_contrato))
                conn.commit()
            conn.close()
            return [True,'Registro Exitoso!']
        except Exception as ex:
            print(ex)
            return [False,ex]
    
    @classmethod
    def actualizar_pago_contrato(cls, pago_contrato):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""UPDATE pago_contrato 
                SET observacion = %s, fecha_registro = NOW(), estado = 'R' 
                WHERE id = %s;""", 
                (pago_contrato.observacion,pago_contrato.id))
                conn.commit()
            conn.close()
            return [True,'Registro Exitoso!']
        except Exception as ex:
            print(ex)
            return [False,ex]
            
    @classmethod      
    def traer_servicio_abonado(cls):    
        try:
            conn = conectar_bd()
            datos_consulta = []
            with conn.cursor() as cursor:
                cursor.execute("""SELECT sa.id,sa.nombre,sa.precio,sa.descripcion,sa.estado 
                               FROM servicio_abonado sa WHERE sa.estado = 'A';""")
                resultado = cursor.fetchall()
                for fila in resultado:
                    dato = ServicioAbonado(fila[0], fila[1], fila[2], fila[3], fila[4])
                    datos_consulta.append(dato.convertir_JSON())
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            
    @classmethod    
    def traer_contratos(cls):    
        try:
            conn = conectar_bd()
            datos_consulta = []
            with conn.cursor() as cursor:
                cursor.execute("""SELECT c.id, CONCAT(cl.nombres,' ',cl.apellido_p) as nombre_abonado, 
                            cl.nro_ci, sa.nombre as nombre_servicio_abonado, c.fecha_inicio, c.fecha_fin,c.estado
                            FROM contrato c JOIN cliente cl ON c.id_cliente = cl.id
                            JOIN servicio_abonado sa ON c.id_servicio_abonado = sa.id
                            ORDER BY c.fecha_inicio DESC;""")
                resultado = cursor.fetchall()
                for fila in resultado:
                    dato = {
                        'id': fila[0],
                        'nombre_abonado': fila[1],
                        'nro_ci': fila[2],
                        'nombre_servicio_abonado': fila[3],
                        'fecha_inicio': fecha(fila[4]),
                        'fecha_fin': fecha(fila[5]),
                        'estado': fila[6]
                    }
                    datos_consulta.append(dato)
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            
    @classmethod
    def traer_pago_contrato(cls, nro_ci):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT pc.id,pc.monto,c.fecha_registro,CONCAT(cl.nombres,' ',cl.apellido_p) as nombre_abonado, 
                               sa.nombre as servicio_abonado
                FROM contrato c JOIN pago_contrato pc ON c.id = pc.id_contrato
                JOIN cliente cl ON c.id_cliente = cl.id
                JOIN servicio_abonado sa ON c.id_servicio_abonado = sa.id
                WHERE cl.nro_ci = %s AND c.estado= 'E';""", (nro_ci,))
                resultado = cursor.fetchone()
                datos_consulta = False
                if resultado:
                    dato= {
                        'id_pago_contrato': resultado[0],
                        'monto': resultado[1],
                        'fecha_registro': fecha_hora(resultado[2]),
                        'nombre_abonado': resultado[3],
                        'servicio_abonado': resultado[4]
                        }
                    datos_consulta= dato
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)