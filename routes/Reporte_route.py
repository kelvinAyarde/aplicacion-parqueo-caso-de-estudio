from flask import Blueprint, jsonify, request, session,redirect, render_template, url_for
from utils.mensaje_error import formato_error
# Entidades
#from models.entidades.Cliente_ent import Cliente
# Modelos
from models.Reporte_model import Reporte_modelo

reporte = Blueprint('reporte_bp', __name__)

@reporte.route('/')
def reporte_principal():
    return render_template('reporte/reporte.html')

@reporte.route('/reporte_veh_est')
def reporte_veh_est():
    return render_template('reporte/reporte_veh_est.html')

@reporte.route('/reporte_sal_veh')
def reporte_sal_veh():
    return render_template('reporte/reporte_sal_veh.html')

@reporte.route('/reporte_con_vig')
def reporte_con_vig():
    return render_template('reporte/reporte_con_vig.html')

@reporte.route('/traer_reporte_veh_est', methods=['GET'])
def traer_reporte_veh_est():
    resultado = Reporte_modelo.reporte_vehiculo_estacionamiento()
    return jsonify(resultado)

@reporte.route('/traer_reporte_sal_veh', methods=['GET'])
def traer_reporte_sal_veh():
    resultado = Reporte_modelo.reporte_salida_vehiculo()
    return jsonify(resultado)

@reporte.route('/traer_reporte_con_vig', methods=['GET'])
def traer_reporte_con_vig():
    resultado = Reporte_modelo.reporte_contrato_vigente()
    return jsonify(resultado)