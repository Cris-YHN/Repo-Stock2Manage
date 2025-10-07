from models.UsuarioModels import UsuarioModel
from entities.UsuarioEntity import Usuario

def registrar_usuario(nombre, apellido, contrasenia, puesto):
    contr_hashed = UsuarioModel.hash_password(contrasenia)
    usuario = Usuario(nombre=nombre, apellido=apellido, contrasenia=contr_hashed, puesto=puesto, activo=0)
    UsuarioModel.insertar(usuario)

def login_usuario(id, contrasenia):
    usuario = UsuarioModel.obtener_por_id(id)
    if usuario and UsuarioModel.check_password(contrasenia, usuario.contrasenia):
        return usuario
    if not usuario:
        return None
    if usuario.activo == 0:
        return None
    return None

def listar_usuarios():
    return UsuarioModel.obtener_todos()

def listar_activos():
    return UsuarioModel.obtener_activos()

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

def buscar_por_apellido(apellido: str):
    return UsuarioModel.buscar_por_apellido(apellido)

def listar_inactivos():
    return UsuarioModel.obtener_inactivos()