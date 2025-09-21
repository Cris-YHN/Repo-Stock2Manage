class Proveedor:
    def __init__(self, id_proveedor=None, nombre_proveedor="", codigo_postal="", provincia="",
                 localidad="", calle="", numero="", telefono=""):
        self.id_proveedor = id_proveedor
        self.nombre_proveedor = nombre_proveedor
        self.codigo_postal = codigo_postal
        self.provincia = provincia
        self.localidad = localidad
        self.calle = calle
        self.numero = numero
        self.telefono = telefono