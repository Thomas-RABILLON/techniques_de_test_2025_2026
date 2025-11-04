class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class PointSet:
    def __init__(self, list_of_point: list):
        self.points = list_of_point
    
    def __len__(self) -> int:
        # TODO
        return 0
    
    def __eq__(self, value) -> bool:
        # TODO
        return False
    
    def to_bytes(self) -> str:
        # TODO
        return ''

    @staticmethod
    def from_bytes(source: str) -> PointSet:
        return PointSet([Point(0.0, 0.0), Point(1.0, 1.0), Point(1.0, 0.0)])
