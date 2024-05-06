from database.db import conectar_bd
from .entidades.Vehiculo_ent import ModeloMarca, VehiculoCliente
from .entidades.Cliente_ent import Cliente

class Cliente_modelo():

    @classmethod
    def registrar_cliente(cls, cliente):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO cliente (nombres, apellido_p, apellido_m, nro_ci, email, 
                               telefono, direccion, estado_contrato) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""", 
                               (cliente.nombres,cliente.apellido_p,cliente.apellido_m,cliente.nro_ci,cliente.email,
                                cliente.telefono,cliente.direccion,cliente.estado_contrato))
                id_cliente = cursor.lastrowid
                conn.commit()
            conn.close()
            return [True,id_cliente]
        except Exception as ex:
            print("registrar_cliente error: " + str(ex))
            return [False,ex]

    @classmethod
    def registrar_nuevo_cliente(cls, cliente, vehiculo):
        try:
            id_cliente = Cliente_modelo.registrar_cliente(cliente)
            id_vehiculo = VehiculoCliente_modelo.registrar_vehiculo(vehiculo)
            if id_cliente[0] == True and id_vehiculo[0] == True:
                reg_vehiculo_cliente = VehiculoCliente_modelo.registrar_vehiculo_cliente(id_vehiculo,id_cliente)
                return reg_vehiculo_cliente
            else:
                return [False, 'Error al registrar nuevo cliente']
        except Exception as ex:
            print(ex)
            return [False, ex]
    
    @classmethod
    def traer_cliente_nro_ci(cls, nro_ci):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT c.id, c.nombres,c.apellido_p,c.apellido_m,c.nro_ci,c.estado_contrato 
                               FROM cliente c WHERE c.nro_ci = %s;""", (nro_ci,))
                resultado = cursor.fetchone()
                datos_consulta = [False, 'No existe un cliente con ese nro_ci']
                if resultado:
                    cliente = Cliente(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4],estado_contrato=resultado[5])
                    datos_consulta = [True,cliente.convertir_JSON()]
            conn.close()
            return datos_consulta
        except Exception as ex:
            print("traer_cliente_nro_ci error: " + str(ex))
            return [False, ex]
    
    @classmethod
    def traer_vehiculo_placa(cls, placa):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""SELECT v.id, v.placa, v.color,CONCAT(mm.modelo,' ', mm.marca) as modelo_marca,
                    CASE
                        WHEN vc.estado = 'A' THEN 'S'
                        ELSE 'N'
                    END AS tiene_propietario
                FROM vehiculo v
                JOIN modelo_marca mm ON mm.id = v.id_modelo_marca
                LEFT JOIN vehiculo_cliente vc ON v.id = vc.id_vehiculo
                WHERE v.placa = %s;""", (placa,))
                resultado = cursor.fetchone()
                datos_consulta = [False, 'No existe un vehiculo con esa placa']
                if resultado:
                    if(resultado[4] == 'S'):
                        datos_consulta = [False, 'El vehiculo ya tiene un propietario!']
                    else:
                        dato = {
                                'id': resultado[0],
                                'placa': resultado[1],
                                'color': resultado[2],
                                'modelo_marca': resultado[3],
                            }
                        datos_consulta = [True,dato]
            conn.close()
            return datos_consulta
        except Exception as ex:
            print("traer_cliente_nro_ci error: " + str(ex))
            return [False, ex]
            
    @classmethod    
    def traer_clientes(cls):    
        try:
            conn = conectar_bd()
            datos_consulta = []
            with conn.cursor() as cursor:
                cursor.execute("""SELECT c.id, c.nombres, CONCAT(c.apellido_p,' ',c.apellido_m) as apellidos, COUNT(vc.id_cliente) as nro_vehiculos, c.nro_ci
                FROM cliente c JOIN vehiculo_cliente vc ON vc.id_cliente = c.id 
                WHERE vc.estado='A'
                GROUP by c.id;""")
                resultado = cursor.fetchall()
                for fila in resultado:
                    dato = {
                        'id': fila[0],
                        'nombres': fila[1],
                        'apellidos': fila[2],
                        'nro_vehiculos': fila[3],
                        'nro_ci': fila[4]
                    }
                    datos_consulta.append(dato)
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            
class VehiculoCliente_modelo():

    @classmethod
    def registrar_vehiculo(cls, vehiculo):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO vehiculo (placa, color, id_modelo_marca) VALUES (%s, %s, %s);""", 
                (vehiculo.placa,vehiculo.color,vehiculo.id_modelo_marca))
                id_vehiculo = cursor.lastrowid
                conn.commit()
            conn.close()
            return [True,id_vehiculo]
        except Exception as ex:
            return [False,ex]
        
    @classmethod
    def registrar_vehiculo_cliente(cls,vehiculo_cliente):
        try:
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute("""INSERT INTO vehiculo_cliente (estado, id_vehiculo, id_cliente) VALUES ('A', %s, %s)""", 
                (vehiculo_cliente.id_vehiculo,vehiculo_cliente.id_cliente))
                conn.commit()
            conn.close()
            return [True,'Registro exitoso!']
        except Exception as ex:
            print("registrar_vehiculo_cliente error: " + str(ex))
            return [False,ex]
            
    @classmethod      
    def traer_modelo_marca(cls):    
        try:
            conn = conectar_bd()
            datos_consulta = []
            with conn.cursor() as cursor:
                cursor.execute("""SELECT m.id,m.modelo,m.marca FROM modelo_marca m;""")
                resultado = cursor.fetchall()
                for fila in resultado:
                    dato = ModeloMarca(fila[0], fila[1], fila[2])
                    datos_consulta.append(dato.convertir_JSON())
            conn.close()
            return datos_consulta
        except Exception as ex:
            print(ex)
            
        