from flask import Blueprint, jsonify, request, session,redirect, render_template, url_for
# Entidades
from models.entidades.Cliente_ent import Cliente
from models.entidades.Contrato_ent import Contrato,PagoContrato
# Modelos
from models.Contrato_model import Contrato_modelo

contrato = Blueprint('contrato_bp', __name__)

@contrato.route('/')
def contrato_principal():
    return render_template('contrato/contrato.html')
    
@contrato.route('/contrato_registro', methods=['GET', 'POST'])
def contrato_registro():
    if request.method == 'POST':
        #data es el tipo de datos que traera el post
        data = request.json
        fecha_inicio = data.get('fecha_inicio')
        id_servicio_abonado = data.get('id_servicio_abonado')
        id_cliente = data.get('id_cliente')
        cliente_estado_contrato = data.get('cliente_estado_contrato')
        if id_cliente == '':
            respuesta = {'exito': False, 'titulo': 'Error', 'mensaje': 'Ingrese un cliente valido'}
            return jsonify(respuesta) 
        if cliente_estado_contrato == 'A':
            respuesta = {'exito': False, 'titulo': 'Error', 'mensaje': 'El cliente ya tiene un contrato activo'}
            return jsonify(respuesta) 
        ent_contrato = Contrato(0,fecha_inicio,None,'E',None,id_servicio_abonado,id_cliente)
        resultado = Contrato_modelo.registrar_contrato(ent_contrato)
        if resultado[0] == True:
            respuesta = {'exito':True ,'titulo':'Exito', 'mensaje':resultado[1],
                         'redireccion': '/contrato'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'Error', 'mensaje':resultado[1].args[1]}
            return jsonify(respuesta)
    else:
        return render_template('contrato/reg_contrato.html')
    
@contrato.route('/traer_servicio_abonado', methods=['GET'])
def traer_servicio_abonado():
    resultado = Contrato_modelo.traer_servicio_abonado()
    return jsonify(resultado)

@contrato.route('/traer_contratos', methods=['GET'])
def traer_clientes():
    modelo_marca = Contrato_modelo.traer_contratos()
    return jsonify(modelo_marca)

@contrato.route('/traer_pago_contrato/<nro_ci>', methods=['GET'])
def traer_pago_contrato(nro_ci):
    resultado = Contrato_modelo.traer_pago_contrato(nro_ci)
    if resultado != False:
        respuesta = {'exito':True ,'contenido': resultado}
        return jsonify(respuesta)
    else:
        respuesta = {'exito':False ,'contenido':'No tiene contrato en Espera!'}
        return jsonify(respuesta)
    
@contrato.route('/actualizar_pago_contrato', methods=['GET', 'PUT'])
def actualizar_pago_contrato():
    if request.method == 'PUT':
        data = request.json
        id_pago_contrato = data.get('id_pago_contrato')
        observacion = data.get('observacion')
        if id_pago_contrato == '':
            respuesta = {'exito': False, 'titulo': 'Error', 'mensaje': 'ingrese un abonado valido'}
            return jsonify(respuesta) 
        ent_pago_contrato = PagoContrato(id_pago_contrato,None,observacion,None,None,None)
        resultado = Contrato_modelo.actualizar_pago_contrato(ent_pago_contrato)
        if resultado[0] == True:
            respuesta = {'exito':True ,'titulo':'Exito', 'mensaje':resultado[1],
                         'redireccion': '/contrato'}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'Error', 'mensaje':resultado[1].args[1]}
            return jsonify(respuesta)
    else:
        return render_template('contrato/reg_pago_contrato.html')
