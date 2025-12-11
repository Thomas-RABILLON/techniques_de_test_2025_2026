import struct

from triangulator.models.Triangle import Triangle
from pointset_manager.models.PointSet import PointSet

class Triangles:
    def __init__(self, list_of_triangle: list, pointset: PointSet):
        if type(pointset) != PointSet:
            raise TypeError
        
        self.triangles: list = list_of_triangle
        self.ps: PointSet = pointset
    
    def __len__(self) -> int:
        return len(self.triangles)
    
    def add_triangles(self, triangle: Triangle) -> None:
        if type(triangle) != Triangle:
            raise TypeError
        
        self.triangles.append(triangle)

    def to_bytes(self) -> str:
        if len(self.triangles) <= 0:
            raise ValueError

        res = self.ps.to_bytes()
        res += struct.pack("<L", len(self.triangles))
        
        for t in self.triangles:
            res += t.to_bytes()

        return res
    
    @staticmethod
    def from_bytes(source: bytes|bytearray) -> Triangles:
        if type(source) != bytes and type(source) != bytearray:
            raise TypeError
        
        try:
            ps_nb_points = struct.unpack("<L", source[:4])[0]
        except:
            raise ValueError
        
        ps_len = 4 + ps_nb_points * 8
        ps = PointSet.from_bytes(source[:ps_len])

        try:
            nb_triangles = struct.unpack("<L", source[ps_len:ps_len+4])[0]
        except:
            raise ValueError
        
        expected_len = ps_len + 4 + nb_triangles * 12
        if len(source) != expected_len:
            raise ValueError

        triangles = []
        for i in range(ps_len + 4, expected_len, 12):
            triangles.append(Triangle.from_bytes(source[i:i+12], ps))
        
        return Triangles(triangles, ps)
