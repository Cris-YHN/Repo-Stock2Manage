class Usuario:
    def __init__(self, id_usuario=None, nombre="", apellido="", contrasenia="", puesto="", activo=1, timestamp=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.contrasenia = contrasenia
        self.puesto = puesto
        self.activo = activo
        self.timestamp = timestamp