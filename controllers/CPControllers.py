from models.CPModels import CodePostalModel

def listar_cp():
    return CodePostalModel.obtener_todos()

def Buscar_proveedor_por_nombre(ciudad):
    return CodePostalModel.Obtener_por_nombre(ciudad)