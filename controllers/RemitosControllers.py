from models.RemitosModels import RemitoModel
from entities.RemitosEntity import Remito, RemitoDetalle

def crear_remito(fecha, idprov, detalles):  #para la funcion dentro de stock_view
    remito = Remito(fecha_remito=fecha, id_proveedor=idprov, detalles=detalles)
    return RemitoModel.insertar(remito)

def listar_remitos():
    return RemitoModel.obtener_todos()

def Buscar_remito_por_id(idrem):
    return RemitoModel.obtener_por_ID(idrem)

def modificar_proveedor(id_remito, Id_proveedor):
    RemitoModel.actualizar_proveedor(id_remito, Id_proveedor)

def listar_detalles_por_remito(id_remito):
    return RemitoModel.obtener_detalles_por_remito(id_remito)