class Material:
    def __init__(self, id_material=None, nombre="", stock_disponible=0,
                 id_proveedor=None, nombre_proveedor="", max_ingreso=0, activo=1):
        self.id_material = id_material
        self.nombre = nombre
        self.stock_disponible = stock_disponible
        self.id_proveedor = id_proveedor
        self.nombre_proveedor = nombre_proveedor
        self.max_ingreso = max_ingreso
        self.activo = activo