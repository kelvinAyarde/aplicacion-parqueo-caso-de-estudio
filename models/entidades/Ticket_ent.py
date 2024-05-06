from utils import formato_time
class Ticket:
    def __init__(self, id, hora_ingreso, hora_salida, estado, id_lugar, id_vehiculo, id_encargado) -> None:
        self.id = id
        self.hora_ingreso = hora_ingreso
        self.hora_salida = hora_salida
        self.estado = estado
        self.id_lugar = id_lugar
        self.id_vehiculo = id_vehiculo
        self.id_encargado = id_encargado
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'hora_ingreso': formato_time.fecha_hora(self.hora_ingreso),
            'hora_salida': formato_time.fecha_hora(self.hora_salida),
            'estado': self.estado,
            'id_lugar': self.id_lugar,
            'id_vehiculo': self.id_vehiculo,
            'id_encargado': self.id_encargado
        }

class PagoTicketVisitante:
    def __init__(self, id, monto, observacion, fecha_registro, id_servicio_visitante, id_ticket) -> None:
        self.id = id
        self.monto = monto
        self.observacion = observacion
        self.fecha_registro = fecha_registro
        self.id_servicio_visitante = id_servicio_visitante
        self.id_ticket = id_ticket
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'monto': self.monto,
            'observacion': self.observacion,
            'fecha_registro': self.fecha_registro,
            'id_servicio_visitante': self.id_servicio_visitante,
            'id_ticket': self.id_ticket
        }
