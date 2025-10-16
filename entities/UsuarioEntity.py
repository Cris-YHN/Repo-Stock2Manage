class Usuario:
    def __init__(self, id_usuario=None, nombre="", apellido="", contrasenia="", puesto="", activo=None, timestamp=None, email="", codigohash="", intentos_fallidos=None, fecha_ultimo_intento=""):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.contrasenia = contrasenia
        self.puesto = puesto
        self.activo = activo
        self.timestamp = timestamp
        self.email=email
        self.codigohash = codigohash
        self.intentos_fallidos = intentos_fallidos
        self.fecha_ultimo_intento = fecha_ultimo_intento