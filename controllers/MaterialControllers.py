from models.MaterialModels import MaterialModel
from entities.MaterialEntity import Material

def listar_materiales():
    return MaterialModel.obtener_materiales()

def listar_materiales_activos():
    return MaterialModel.obtener_activos()

def crear_material(nombre, id_proveedor):
    material = Material(nombre=nombre, id_proveedor=id_proveedor)
    MaterialModel.insertar(material)

def modificar_material(id_material, nombre, stock, id_proveedor):
    MaterialModel.actualizar(id_material, nombre, stock, id_proveedor)

def alta_material(id_material):
    MaterialModel.cambiar_estado(id_material, 1)

def baja_material(id_material):
    MaterialModel.cambiar_estado(id_material, 0)

def Carga_Materiales_delRemito(id_material, cantidad):
    MaterialModel.cargar_remito(id_material, cantidad)

def listar_materiales_escasos():
    return MaterialModel.obtener_escasos()

def listar_materiales_inactivos():
    return MaterialModel.obtener_inactivos()

def buscar_nombre(namemat):
    return MaterialModel.obtener_por_nombre(namemat)

def verificar_existencia(idmat):
    return MaterialModel.material_existe(idmat)

def uso_material(cantidad, idmat):
    MaterialModel.descontar_material(cantidad, idmat)