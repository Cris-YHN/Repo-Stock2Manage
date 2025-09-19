from models.UsuarioModels import UsuarioModel
from entities.UsuarioEntity import Usuario

def registrar_usuario(nombre, apellido, contrasenia, puesto):
    usuario = Usuario(nombre=nombre, apellido=apellido, contrasenia=contrasenia, puesto=puesto, activo=0)
    UsuarioModel.insertar(usuario)

def login_usuario(id, contrasenia):
    usuario = UsuarioModel.obtener_por_id(id)
    if usuario and usuario.contrasenia == contrasenia:
        return usuario
    return None

def listar_usuarios():
    return UsuarioModel.obtener_todos()

def listar_solicitudes():
    return UsuarioModel.obtener_solicitudes()

def aprobar_usuario(id_usuario):
    UsuarioModel.cambiar_estado_usuario(id_usuario, 1)

def rechazar_usuario(id_usuario):
    UsuarioModel.eliminar_usuario(id_usuario)

def baja_usuario(id_usuario):
    UsuarioModel.cambiar_estado_usuario(id_usuario, 2)

def alta_usuario(id_usuario):
    UsuarioModel.cambiar_estado_usuario(id_usuario, 1)

def modificar_usuario(id_usuario, nombre, apellido, puesto):
    UsuarioModel.actualizar_usuario(id_usuario, nombre, apellido, puesto)

def buscar_id(id_usuario):
    return UsuarioModel.obtener_busqueda_por_id(id_usuario)

def listar_inactivos():
    return UsuarioModel.obtener_inactivos()