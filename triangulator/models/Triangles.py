from pointset_manager.models.PointSet import PointSet

class Triangle:
    def __init__(self, indices: tuple):
        self.indices: tuple = indices
    
    def __eq__(self, value):
        return False
    
    def to_bytes(self) -> str:
        # TODO
        return ''
    
    @staticmethod
    def from_bytes(source: str, pointset: PointSet) -> Triangle:
        # TODO
        return None

class Triangles:
    def __init__(self, list_of_triangle: list):
        self.triangles: list = list_of_triangle
    
    def __len__(self) -> int:
        # TODO
        return 0
    
    def __eq__(self, value):
        # TODO
        return False
    
    def add_triangles(self, triangle: Triangle) -> None:
        self.triangles.append(triangle)

    def to_bytes(self) -> str:
        # TODO
        return ''
    
    @staticmethod
    def from_bytes(source: str) -> Triangles:
        # TODO
        return None
