class Manufactura:
    def __init__(self,id_manufactura=None, nombre=""):
        self.id_manufactura = id_manufactura
        self.nombre = nombre


class ManufacturaDetalle:
    def __init__(self, id_manufactura=None, id_paso=None, id_material=None, nombre="", cantidad_necesaria=None):
        self.id_manufactura = id_manufactura
        self.id_paso = id_paso
        self.id_material = id_material
        self.nombre = nombre
        self.cantidad_necesaria = cantidad_necesaria
