import struct

from pointset_manager.models.Point import Point

class PointSet:
    def __init__(self, list_of_point: list):
        self.points: list = list_of_point
    
    def __len__(self) -> int:
        return len(self.points)
    
    def add_point(self, point: Point) -> None:
        if type(point) != Point:
            raise TypeError
        
        self.points.append(point)

    def to_bytes(self) -> str:
        if len(self.points) <= 0:
            raise ValueError

        res = struct.pack("<L", len(self.points))

        for point in self.points:
            res += point.to_bytes()

        return res

    @staticmethod
    def from_bytes(source: bytes|bytearray) -> PointSet:
        if type(source) != bytes and type(source) != bytearray:
            raise TypeError
        if len(source) < 4:
            raise ValueError
        
        try:
            nb_points = struct.unpack("<L", source[:4])[0]
        except:
            raise ValueError
        
        excepted_len = 4 + nb_points * 8
        if len(source) != excepted_len:
            raise ValueError
        
        points = []
        for i in range(4, excepted_len, 8):
            points.append(Point.from_bytes(source[i:i+8]))

        return PointSet(points)
