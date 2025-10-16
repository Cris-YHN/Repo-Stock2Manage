from models.UsuarioModels import UsuarioModel
from entities.UsuarioEntity import Usuario

def registrar_usuario(nombre, apellido, contrasenia, email, puesto):
    contr_hashed = UsuarioModel.hash_password(contrasenia)
    usuario = Usuario(nombre=nombre, apellido=apellido, contrasenia=contr_hashed, email=email, puesto=puesto, activo=0)
    UsuarioModel.insertar(usuario)
    return usuario

def login_usuario(id, contrasenia):
    usuario = UsuarioModel.obtener_por_id(id)
    if not usuario:
        return None
    if usuario and UsuarioModel.check_password(contrasenia, usuario.contrasenia):
        UsuarioModel.resetear_intentos(id)
        return usuario
    else:
        UsuarioModel.registrar_intento_fallido(id)
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

def modificar_usuario(id_usuario, nombre, apellido, email, puesto):
    UsuarioModel.actualizar_usuario(id_usuario, nombre, apellido, email, puesto)

def buscar_por_apellido(apellido: str):
    return UsuarioModel.buscar_por_apellido(apellido)

def listar_inactivos():
    return UsuarioModel.obtener_inactivos()

def enviar_codigo_recuperacion(id_usuario):
    usuario = UsuarioModel.obtener_por_id(id_usuario)
    if not usuario:
        return None
    codigo = UsuarioModel.generar_codigo_hash(id_usuario)
    UsuarioModel.enviar_codigo_email(usuario.email, codigo)
    return usuario

def verificar_codigo(id_usuario, codigo):
    usuario = UsuarioModel.obtener_por_id(id_usuario)
    if usuario and usuario.codigohash == codigo:
        return True
    return False

def cambiar_contrasenia(id_usuario, nueva_contrasenia):
    usuario = UsuarioModel.obtener_por_id(id_usuario)
    if not usuario:
        return "Usuario no encontrado"
    if UsuarioModel.check_password(nueva_contrasenia, usuario.contrasenia):
        return "No puede usar la misma contraseña anterior"
    hashed = UsuarioModel.hash_password(nueva_contrasenia)
    UsuarioModel.actualizar_contrasenia(id_usuario, hashed)
    return "Contraseña actualizada correctamente"

def obtener_usuario_por_id(id_usuario):
    return UsuarioModel.obtener_por_id(id_usuario)