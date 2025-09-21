from models.ProveedorModels import ProveedorModel
from entities.ProveedorEntity import Proveedor

def listar_proveedores():
    return ProveedorModel.obtener_todos()

def Buscar_proveedor_por_id(id):
    return ProveedorModel.obtener_por_ID(id)

def crear_proveedor(nombre, cp, calle, numero, telefono):
    proveedor = Proveedor(nombre_proveedor=nombre, codigo_postal=cp, calle=calle, numero=numero, telefono=telefono)
    ProveedorModel.insertar(proveedor)
    
def modificar_proveedor(id_prov,nombre_proveedor, codigo_postal, calle, numero, telefono):
    ProveedorModel.actualizar_proveedor(id_prov,nombre_proveedor, codigo_postal, calle, numero, telefono)