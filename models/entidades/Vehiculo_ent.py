class Vehiculo:
    def __init__(self, id=None, placa=None, color=None, id_modelo_marca=None):
        self.id = id
        self.placa = placa
        self.color = color
        self.id_modelo_marca = id_modelo_marca
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'placa': self.placa,
            'color': self.color,
            'id_modelo_marca': self.id_modelo_marca,
        }

class VehiculoCliente:
    def __init__(self, estado, id_vehiculo, id_cliente):
        self.estado = estado
        self.id_vehiculo = id_vehiculo
        self.id_cliente = id_cliente
    
    def convertir_JSON(self):
        return {
            'estado': self.estado,
            'id_vehiculo': self.id_vehiculo,
            'id_cliente': self.id_cliente,
        }

class ModeloMarca:
    def __init__(self, id, modelo, marca):
        self.id = id
        self.modelo = modelo
        self.marca = marca
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'modelo': self.modelo,
            'marca': self.marca
        }

