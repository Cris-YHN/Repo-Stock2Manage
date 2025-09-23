class Remito:
    def __init__(self, id_remito=None, fecha_remito="", id_proveedor=None,nombre_proveedor="", detalles=None):
        self.id_remito = id_remito
        self.fecha_remito = fecha_remito
        self.id_proveedor = id_proveedor
        self.nombre_proveedor = nombre_proveedor
        self.detalles = detalles if detalles is not None else []  # lista de objetos RemitoDetalle

class RemitoDetalle:
    def __init__(self, id_remito=None, id_material=None, cantidad=None):
        self.id_remito = id_remito
        self.id_material = id_material
        self.cantidad = cantidad