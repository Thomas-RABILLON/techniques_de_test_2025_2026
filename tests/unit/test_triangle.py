import struct
import pytest

from triangulator.models.Triangles import Triangle
from pointset_manager.models.PointSet import PointSet
from pointset_manager.models.Point import Point

class TestTriangle:
    @pytest.fixture
    def pointset_3_points(self) -> PointSet:
        return PointSet([Point(0.0, 0.0), Point(1.0, 1.0), Point(2.0, 2.0)])
    
    @pytest.fixture
    def pointset_1_point(self) -> PointSet:
        return PointSet([Point(0.0, 0.0)])

    def test_triangle_init_invalid(self):
        with pytest.raises(TypeError):
            Triangle((0, None, 1))

        with pytest.raises(ValueError):
            Triangle((0, 1))
        
        with pytest.raises(ValueError):
            Triangle((0, 1, 2, 3))

    def test_triangle_to_bytes_valid(self):
        t = Triangle((0, 1, 2))
        b = t.to_bytes()
        assert len(b) == 12

        expected = struct.pack("<LLL", 0, 1, 2)
        assert b == expected

    def test_from_bytes_valid(self, pointset_3_points: PointSet):
        b = struct.pack("<LLL", 2, 1, 0)

        t = Triangle.from_bytes(b, pointset_3_points)
        assert t.indices == (2, 1, 0)
    
    def test_from_bytes_invalied_index(self, pointset_3_points: PointSet):
        b = struct.pack("<LLL", 0, 5, 1)
        with pytest.raises(IndexError):
            Triangle.from_bytes(b, pointset_3_points)

    def test_from_bytes_invalid_source_len(self, pointset_1_point: PointSet):
        with pytest.raises(ValueError):
            Triangle.from_bytes(b"\x00", pointset_1_point)
    
    def test_from_bytes_invalid_len(self, pointset_1_point: PointSet):
        with pytest.raises(ValueError):
            Triangle.from_bytes(b"\x00\x00\x00", pointset_1_point)
    
    def test_from_bytes_invalid_source_type(self, pointset_1_point: PointSet):
        with pytest.raises(TypeError):
            Triangle.from_bytes("pas des bytes", pointset_1_point)

    def test_from_bytes_pointset_none(self):
        b = struct.pack("<LLL", 0, 1, 2)

        with pytest.raises(ValueError):
            Triangle.from_bytes(b, None)

