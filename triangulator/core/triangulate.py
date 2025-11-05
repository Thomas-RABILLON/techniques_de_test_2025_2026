from pointset_manager.models.PointSet import PointSet
from triangulator.models.Triangles import Triangles

def get_pointset_by_id(id_pointset: int):
    return None

def calcul_triangle(pointset: PointSet):
    return None

def triangulate(id_pointset: int):
    pointset: PointSet = get_pointset_by_id(id_pointset)

    triangles: Triangles = calcul_triangle(pointset)
