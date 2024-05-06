from flask import session
from database.db import conectar_bd

class SesionUsuario():

    @classmethod
    def verificar_usuario(cls, usu):
        try:
            autentificado = False
            conn = conectar_bd()
            with conn.cursor() as cursor:
                cursor.execute('call verificar_credencial(%s, %s)', (usu.usuario, usu.password))
                resultado = cursor.fetchone()
                if resultado:
                    SesionUsuario.guardar_sesion(resultado)
                    autentificado = True
            conn.close()
            return autentificado
        except Exception as ex:
            print(ex)
    
    def guardar_sesion(datos_usu):
        session['sesion_abierta'] = True
        #---------------
        session['id_personal'] = int(datos_usu[0])
        session['id_rol'] = int(datos_usu[1])
        #---------------
        session['nombres'] = datos_usu[2]
        session['apellido_1'] = datos_usu[3]
        session['apellido_2'] = datos_usu[4] if datos_usu[4] is not None else '' # si no es null entonces se pasa en blanco ''
        session['usuario'] = datos_usu[5]
        session['rol'] = datos_usu[6]

    def cerrar_sesion():
        session.clear()