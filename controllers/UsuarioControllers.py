from models.UsuarioModels import UsuarioModel
from entities.UsuarioEntity import Usuario

def registrar_usuario(nombre, apellido, contrasenia, puesto):
    usuario = Usuario(nombre=nombre, apellido=apellido, contrasenia=contrasenia, puesto=puesto, activo=1)
    UsuarioModel.insertar(usuario)

def login_usuario(id, contrasenia):
    usuario = UsuarioModel.obtener_por_id(id)
    if usuario and usuario.contrasenia == contrasenia:
        return usuario
    return None