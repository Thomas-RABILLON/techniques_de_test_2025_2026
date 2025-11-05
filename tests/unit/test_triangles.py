import pytest

from triangulator.models.Triangles import Triangles, Triangle
from pointset_manager.models.PointSet import PointSet, Point

class TestTriangles:
    @pytest.fixture
    def pointset(self) -> PointSet:
        return PointSet([Point(0.0, 0.0), Point(1.0, 1.0), Point(1.0, 0.0)])

    @pytest.fixture
    def correct_triangle(self) -> Triangle:
        return Triangle((0, 1, 2))
    
    @pytest.fixture
    def triangle_correct_bytes(self) -> str:
        return ''

    def test_triangle_to_bytes(self, correct_triangle: Triangle, triangle_correct_bytes: str):
        assert correct_triangle.to_bytes() == triangle_correct_bytes