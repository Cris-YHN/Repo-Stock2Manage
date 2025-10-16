from models.CPModels import CodePostalModel

def listar_cp():
    return CodePostalModel.obtener_todos()

def Buscar_cp_por_nombre(ciudad):
    return CodePostalModel.Obtener_por_nombre(ciudad)