
class Cliente():
    def __init__(self, id=None, nombres=None, apellido_p=None, apellido_m=None, nro_ci=None, email=None, telefono=None, direccion=None, estado_contrato=None):
        self.id = id
        self.nombres = nombres
        self.apellido_p = apellido_p
        self.apellido_m = apellido_m
        self.nro_ci = nro_ci
        self.email = email
        self.telefono = telefono
        self.direccion = direccion
        self.estado_contrato = estado_contrato
    
    def convertir_JSON(self):
        return {
            'id': self.id,
            'nombres': self.nombres,
            'apellido_p': self.apellido_p,
            'apellido_m': self.apellido_m,
            'nro_ci': self.nro_ci,
            'email': self.email,
            'telefono': self.telefono,
            'direccion': self.direccion,
            'estado_contrato': self.estado_contrato
        }

