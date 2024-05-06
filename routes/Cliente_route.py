from flask import Blueprint, jsonify, request, session,redirect, render_template, url_for
from utils.mensaje_error import formato_error
# Entidades
from models.entidades.Cliente_ent import Cliente
from models.entidades.Vehiculo_ent import Vehiculo, VehiculoCliente
# Modelos
from models.Cliente_model import Cliente_modelo,VehiculoCliente_modelo

cliente = Blueprint('cliente_bp', __name__)

@cliente.route('/')
def cliente_principal():
    return render_template('cliente/cliente.html')

@cliente.route('/registro', methods=['GET', 'POST'])
def cliente_nuevo_registro():
    if request.method == 'POST':
        #data es el tipo de datos que traera el post
        data = request.json
        #cliente
        nombres = data.get('nombres')
        apellido_p = data.get('apellido_p')
        apellido_m = data.get('apellido_m')
        nro_ci = data.get('nro_ci')
        email = data.get('email')
        telefono = data.get('telefono')
        direccion = data.get('direccion')
        ent_cliente = Cliente(0, nombres, apellido_p, apellido_m, nro_ci,email,telefono,direccion,'I')
        #------------
        resultado = Cliente_modelo.registrar_cliente(ent_cliente)
        if resultado[0] == True:
            respuesta = {'exito':True ,'titulo':'Exito', 'mensaje': 'Registro exitoso',
                         'redireccion': '/cliente'}
            return jsonify(respuesta)
        else:
            mensaje_error= formato_error(resultado[1])
            respuesta = {'exito':False ,'titulo':'Error', 'mensaje': mensaje_error}
            return jsonify(respuesta)
    else:
        return render_template('cliente/reg_cliente.html')
    
@cliente.route('/vehiculo/modelo_marca')
def traer_modelo_marca():
    modelo_marca = VehiculoCliente_modelo.traer_modelo_marca()
    return jsonify(modelo_marca)

@cliente.route('/registro_vehiculo', methods=['GET', 'POST'])
def registro_vehiculo():
    if request.method == 'POST':
        #data es el tipo de datos que traera el post
        data = request.json
        #vehiculo
        placa = data.get('placa')
        color = data.get('color')
        id_modelo_marca = data.get('id_modelo_marca')
        ent_vehiculo = Vehiculo(0,placa,color,id_modelo_marca)
        resultado = VehiculoCliente_modelo.registrar_vehiculo(ent_vehiculo)
        if resultado[0] == True:
            respuesta = {'exito':True ,'titulo':'Exito', 'mensaje':'Registro exitoso!',
                         'redireccion': '/cliente'}
            return jsonify(respuesta)
        else:
            mensaje_error= formato_error(resultado[1])
            respuesta = {'exito':False ,'titulo':'Error', 'mensaje':mensaje_error}
            return jsonify(respuesta)
    else:
        return render_template('cliente/reg_vehiculo.html')
    
@cliente.route('/traer_cliente_nro_ci/<nro_ci>', methods=['GET'])
def traer_cliente_nro_ci(nro_ci):
    resultado = Cliente_modelo.traer_cliente_nro_ci(nro_ci)
    if resultado[0] == True:
        respuesta = {'exito':True ,'contenido': resultado[1]}
        return jsonify(respuesta)
    else:
        respuesta = {'exito':False ,'contenido':'no existe el cliente!'}
        return jsonify(respuesta)
    
@cliente.route('/traer_clientes', methods=['GET'])
def traer_clientes():
    clientes = Cliente_modelo.traer_clientes()
    return jsonify(clientes)

@cliente.route('/registro_vehiculo_cliente', methods=['GET', 'POST'])
def registro_vehiculo_cliente():
    if request.method == 'POST':
        #data es el tipo de datos que traera el post
        data = request.json
        id_cliente = data.get('id_cliente')
        id_vehiculo = data.get('id_vehiculo')
        if id_cliente == '' or id_vehiculo == '':
            respuesta = {'exito':False ,'titulo':'Error', 'mensaje':'Ingrese datos validos'}
            return jsonify(respuesta)
        
        ent_vehiculo_cliente = VehiculoCliente('A',id_vehiculo,id_cliente)
        resultado = VehiculoCliente_modelo.registrar_vehiculo_cliente(ent_vehiculo_cliente)
        if resultado[0] == True:
            respuesta = {'exito':True ,'titulo':'Exito', 'mensaje':resultado[1],
                         'redireccion': '/cliente'}
            return jsonify(respuesta)
        else:
            mensaje_error= formato_error(resultado[1])
            respuesta = {'exito':False ,'titulo':'Error', 'mensaje':mensaje_error}
            return jsonify(respuesta)
    else:
        return render_template('cliente/reg_vehiculo_cliente.html')
    
@cliente.route('/traer_vehiculo_placa/<placa>', methods=['GET'])
def traer_vehiculo_placa(placa):
    resultado = Cliente_modelo.traer_vehiculo_placa(placa)
    if resultado[0] == True:
        respuesta = {'exito':True ,'contenido': resultado[1]}
        return jsonify(respuesta)
    else:
        respuesta = {'exito':False ,'contenido':resultado[1]}
        return jsonify(respuesta)