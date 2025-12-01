class Point:
    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
    
    def __eq__(self, value) -> bool:
        # TODO
        return False
    
    def to_bytes(self) -> str:
        # TODO
        return ''
    
    @staticmethod
    def from_bytes(source: str) -> Point:
        # TODO
        return None

class PointSet:
    def __init__(self, list_of_point: list):
        self.points: list = list_of_point
    
    def __len__(self) -> int:
        # TODO
        return 0
    
    def __eq__(self, value) -> bool:
        # TODO
        return False
    
    def add_point(self, point: Point) -> None:
        self.points.append(point)

    def to_bytes(self) -> str:
        # TODO
        return ''

    @staticmethod
    def from_bytes(source: str) -> PointSet:
        return None
