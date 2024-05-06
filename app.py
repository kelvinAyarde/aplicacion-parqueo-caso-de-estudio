from flask import Flask
from flask_mysqldb import MySQL
from config import ConfigDesarrollo
#rutas
from routes import Inicio_route,Cliente_route,Contrato_route,Ticket_route,Reporte_route

app = Flask(__name__)

if __name__ == '__main__':
    app.config.from_object(ConfigDesarrollo)
    mysql = MySQL(app)
    #blueprints
    app.register_blueprint(Inicio_route.inicio, url_prefix='/')
    app.register_blueprint(Cliente_route.cliente, url_prefix='/cliente')
    app.register_blueprint(Contrato_route.contrato, url_prefix='/contrato')
    app.register_blueprint(Ticket_route.ticket, url_prefix='/ticket')
    app.register_blueprint(Reporte_route.reporte, url_prefix='/reporte')
    #---------------
    app.run()
