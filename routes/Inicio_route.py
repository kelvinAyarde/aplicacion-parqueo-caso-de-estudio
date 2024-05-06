from flask import Blueprint, jsonify, request, session,redirect, render_template, url_for

# Entidades
from models.entidades.Usuario_ent import Usuario
# Modelos
from models.Inicio_model import SesionUsuario

inicio = Blueprint('inicio_bp', __name__)

@inicio.route('/')
def home():
    if 'sesion_abierta' in session:
        return render_template('inicio/base.html')
    else:      
        return redirect(url_for('inicio_bp.login'))

@inicio.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        ent_usuario = Usuario(0, usuario, password, None, None, None)
        autentificacion = SesionUsuario.verificar_usuario(ent_usuario)
        if autentificacion:
            respuesta = {'exito':True ,'titulo':'exito', 'mensaje':'credenciales correctas!',
                         'redireccion': url_for('inicio_bp.home')}
            return jsonify(respuesta)
        else:
            respuesta = {'exito':False ,'titulo':'error', 'mensaje':'creedenciales incorrectas!'}
            return jsonify(respuesta)
    else:
        return render_template('inicio/login.html')

@inicio.route('/cerrar_sesion')
def cerrar_sesion():
    SesionUsuario.cerrar_sesion()
    return redirect(url_for('inicio_bp.home'))