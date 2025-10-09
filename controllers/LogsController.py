from models.LogsModels import LogsModel
from entities.LogsEntity import logs
import socket

def registrar(usuario, accion, nivel="INFO"):
    if not isinstance(usuario, str):
        try:
            usuario = usuario.nombre  # o usuario.username según tu entidad
        except AttributeError:
            usuario = str(usuario)
    equipo = socket.gethostname()
    log = logs(usuario=usuario, accion=accion, nivel=nivel, equipo=equipo)
    LogsModel.insertar_log(log)

def listar_todos():
    return LogsModel.obtener_logs()
