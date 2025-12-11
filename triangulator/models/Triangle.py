import struct

from pointset_manager.models.PointSet import PointSet

class Triangle:
    def __init__(self, indices: tuple):
        if len(indices) != 3:
            raise ValueError

        for i in indices:
            if type(i) != int:
                raise TypeError

        self.indices: tuple = indices
    
    def to_bytes(self) -> str:
        return struct.pack("<LLL", self.indices[0], self.indices[1], self.indices[2])
    
    @staticmethod
    def from_bytes(source: bytes|bytearray, pointset: PointSet) -> Triangle:
        if type(source) != bytes and type(source) != bytearray:
            raise TypeError
        if len(source) != 12:
            raise ValueError
        if pointset is None:
            raise ValueError

        try:
            indices = struct.unpack("<LLL", source)
        except:
            raise ValueError
        
        try:
            for i in indices:
                pointset.points[i]
        except:
            raise IndexError
        
        return Triangle(indices)