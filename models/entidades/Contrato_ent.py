class ServicioAbonado():
    def __init__(self, id, nombre, precio, descripcion, estado) -> None:
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.estado = estado
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'descripcion': self.descripcion,
            'estado': self.estado
        }

class Contrato:
    def __init__(self, id=None, fecha_inicio=None, fecha_fin=None, estado=None, fecha_registro=None, 
                 id_servicio_abonado=None, id_cliente=None):
        self.id = id
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.fecha_registro = fecha_registro
        self.id_servicio_abonado = id_servicio_abonado
        self.id_cliente = id_cliente

    def convertir_JSON(self):
        return {
            'id': self.id,
            'fecha_inicio': self.fecha_inicio,
            'fecha_fin': self.fecha_fin,
            'estado': self.estado,
            'fecha_registro': self.fecha_registro,
            'id_servicio_abonado': self.id_servicio_abonado,
            'id_cliente': self.id_cliente
        }

class PagoContrato:
    def __init__(self, id, monto, observacion, fecha_registro, estado, id_contrato) -> None:
        self.id = id
        self.monto = monto
        self.observacion = observacion
        self.fecha_registro = fecha_registro
        self.estado = estado
        self.id_contrato = id_contrato
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'monto': self.monto,
            'observacion': self.observacion,
            'fecha_registro': self.fecha_registro,
            'estado': self.estado,
            'id_contrato': self.id_contrato
        }