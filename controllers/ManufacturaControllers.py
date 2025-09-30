from models.ManufacturaModels import ManufacturaModel
from entities.ManufacturaEntity import Manufactura, ManufacturaDetalle

def crear_manufactura(nombre):
    manufact = Manufactura(nombre=nombre)
    return ManufacturaModel.insertar(manufact)

def listar_manufactura():
    return ManufacturaModel.obtener_manufacturas()

def listar_pasos(idmanu):
    return ManufacturaModel.obtener_pasos(idmanu)

def Buscar_manufactura_por_nombre(namemanu):
    return ManufacturaModel.obtener_por_nombre(namemanu)

def modificar_manufactura(idmanu, nombre):
    return ManufacturaModel.actualizar_manufactura(nombre, idmanu)

def crear_paso(id_manufactura: int, id_paso: int, id_material: int, cantidad_necesaria: int):
    detalle = ManufacturaDetalle(
        id_manufactura=id_manufactura,
        id_paso=id_paso,
        id_material=id_material,
        cantidad_necesaria=cantidad_necesaria
    )
    return ManufacturaModel.insertar_paso(detalle)

def modificar_paso(id_manufactura: int, id_paso: int, id_material: int, cantidad_necesaria: int):
    detalle = ManufacturaDetalle(
        id_manufactura=id_manufactura,
        id_paso=id_paso,
        id_material=id_material,
        cantidad_necesaria=cantidad_necesaria
    )
    return ManufacturaModel.modificar_paso(detalle)
