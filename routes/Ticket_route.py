from flask import Blueprint, jsonify, request, session,redirect, render_template, url_for
from utils.mensaje_error import formato_error
# Entidades
from models.entidades.Ticket_ent import Ticket
# Modelos
from models.Ticket_model import Ticket_modelo

ticket = Blueprint('ticket_bp', __name__)

@ticket.route('/')
def ticket_principal():
    return render_template('ticket/ticket.html')

@ticket.route('/registrar_ticket', methods=['GET', 'POST'])
def registrar_ticket():
    if request.method == 'POST':
        data = request.json
        id_lugar = data.get('id_lugar')
        id_vehiculo = data.get('id_vehiculo')
        id_encargado = session['id_personal']
        reg_pago = data.get('reg_pago')
        id_cliente = data.get('id_cliente')
        if id_lugar == '' or id_vehiculo == '' or id_encargado == '':
            respuesta = {'exito': False, 'titulo': 'Error', 'mensaje': 'Rellene todos los campos correspondientes!'}
            return jsonify(respuesta) 
        ent_ticket = Ticket(0,None,None,'A',id_lugar,id_vehiculo,id_encargado)
        resultado= Ticket_modelo.registrar_ticket(ent_ticket,id_cliente,reg_pago)
        if resultado[0] == True:
            respuesta = {'exito':True ,'titulo':'Exito', 'mensaje':resultado[1],
                         'redireccion': '/ticket'}
            return jsonify(respuesta)
        else:
            mensaje_error= formato_error(resultado[1])
            respuesta = {'exito':False ,'titulo':'Error', 'mensaje':mensaje_error}
            return jsonify(respuesta)
    else:
        return render_template('ticket/reg_ticket.html')
    
@ticket.route('/buscar_vehiculo_placa_ticket/<placa>', methods=['GET'])
def buscar_vehiculo_placa_ticket(placa):
    resultado = Ticket_modelo.buscar_vehiculo_placa_ticket(placa)
    if resultado[0]:
        respuesta = {'exito':True ,'contenido': resultado[1]}
        return jsonify(respuesta)
    else:
        respuesta = {'exito':False ,'contenido': resultado[1]}
        return jsonify(respuesta)

@ticket.route('/traer_lugares', methods=['GET'])
def traer_lugares():
    resultado = Ticket_modelo.traer_lugares()
    return jsonify(resultado)

@ticket.route('/registrar_pago_ticket', methods=['GET', 'PUT'])
def pago_ticket():
    if request.method == 'PUT':
        data = request.json
        observacion = data.get('observacion')
        monto = data.get('monto')
        id_servicio_visitante = data.get('id_servicio_visitante')
        id_ticket = data.get('id_ticket')
        abonado = data.get('abonado')
        resultado = Ticket_modelo.registro_pago_ticket(observacion,monto,id_servicio_visitante,id_ticket,abonado)
        if resultado[0] == True:
            respuesta = {'exito':True ,'titulo':'Exito', 'mensaje':resultado[1],
                         'redireccion': '/ticket'}
            return jsonify(respuesta)
        else:
            mensaje_error= formato_error(resultado[1])
            respuesta = {'exito':False ,'titulo':'Error', 'mensaje':mensaje_error}
            return jsonify(respuesta)
    else:
        return render_template('ticket/pago_ticket.html')

@ticket.route('/buscar_ticket/<id_ticket>', methods=['GET'])
def buscar_ticket(id_ticket):
    resultado = Ticket_modelo.buscar_ticket(id_ticket)
    if resultado[0] == True:
        respuesta = {'exito':True ,'contenido': resultado[1]}
        return jsonify(respuesta)
    else:
        mensaje_error= formato_error(resultado[1])
        respuesta = {'exito':False ,'contenido': mensaje_error}
        return jsonify(respuesta)

@ticket.route('/traer_servicio_visitante', methods=['GET'])
def traer_servicio_visitante():
    resultado = Ticket_modelo.traer_servicio_visitante()
    return jsonify(resultado)