class Triangle:
    def __init__(self, list_of_point_index: tuple):
        self.list_of_point_index: tuple = list_of_point_index
    
    def to_bytes(self) -> str:
        # TODO
        return ''
    
    @staticmethod
    def from_bytes(source: str) -> Triangle:
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
    
    def addTriangles(self, triangle: Triangle) -> None:
        self.triangles.append(triangle)

    def to_bytes(self) -> str:
        # TODO
        return ''
    
    @staticmethod
    def from_bytes(source: str) -> Triangles:
        # TODO
        return None
