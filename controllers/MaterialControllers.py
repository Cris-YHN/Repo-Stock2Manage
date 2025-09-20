from models.MaterialModels import MaterialModel
from entities.MaterialEntity import Material

def listar_materiales():
    return MaterialModel.obtener_activos()

def crear_material(nombre, id_proveedor):
    material = Material(nombre=nombre, id_proveedor=id_proveedor, activo=1)
    MaterialModel.insertar(material)

def modificar_material(id_material, nombre, stock, id_proveedor):
    MaterialModel.actualizar(id_material, nombre, stock, id_proveedor)

def alta_material(id_material):
    MaterialModel.cambiar_estado(id_material, 1)

def baja_material(id_material):
    MaterialModel.cambiar_estado(id_material, 0)

def crear_remito(id_material, cantidad):
    MaterialModel.chequeo_max_ingreso(id_material, cantidad)

def listar_materiales_escasos():
    return MaterialModel.obtener_escasos()

def listar_materiales_inactivos():
    return MaterialModel.obtener_inactivos()

def buscar_id(id_material):
    return MaterialModel.obtener_busqueda_por_id(id_material)

