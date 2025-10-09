class logs:
    def __init__(self, id=None, usuario=None, accion=None, nivel=None, equipo=None, fecha=None):
        self.id= id
        self.usuario= usuario
        self.accion= accion
        self.nivel= nivel
        self.equipo= equipo
        self.fecha= fecha
    
    def __repr__(self):
        return f"<Log usuario={self.usuario}, accion={self.accion}, nivel={self.nivel}>"