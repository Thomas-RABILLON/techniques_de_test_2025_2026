import struct
import math

class Point:
    def __init__(self, x: float, y: float):
        if type(x) != float:
            raise TypeError
        if type(y) != float:
            raise TypeError
        if math.isnan(x) or math.isinf(x):
            raise ValueError
        if math.isnan(y) or math.isinf(y):
            raise ValueError

        self.x: float = x
        self.y: float = y
    
    def to_bytes(self) -> str:
        return struct.pack("<ff", self.x, self.y)
       
    @staticmethod
    def from_bytes(source: bytes|bytearray) -> Point:
        if type(source) != bytes and type(source) != bytearray:
            raise TypeError
        if len(source) != 8:
            raise ValueError

        try:
            x, y = struct.unpack("<ff", source)
        except:
            raise ValueError
        
        return Point(x, y)