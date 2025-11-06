from models.LogsModels import LogsModel
from entities.LogsEntity import logs
import socket

def registrar(usuario, accion, nivel):
    if not isinstance(usuario, str):
        try:
            user = usuario.nombre + " " + usuario.apellido  # o usuario.username según tu entidad
        except AttributeError:
            user = str(usuario)
    equipo = socket.gethostname()
    log = logs(usuario=user, accion=accion, nivel=nivel, equipo=equipo)
    LogsModel.insertar_log(log)

def listar_todos():
    return LogsModel.obtener_logs()

def listar_por_nivel(nivel):
    return LogsModel.obtener_por_nivel(nivel)

def listar_login_y_registro():
    todos = LogsModel.obtener_logs()
    return [l for l in todos if l.nivel.upper() in ("LOGIN", "REGISTRO")]


