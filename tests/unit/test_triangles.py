import struct
import pytest

from triangulator.models.Triangles import Triangles, Triangle
from pointset_manager.models.PointSet import PointSet, Point

class TestTriangles:
    @pytest.fixture
    def ps(self):
        return PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0)])

    def test_triangles_init_and_len(self):
        t = Triangles([Triangle((0, 1, 2))])
        assert len(t) == 1

    def test_triangles_to_bytes_and_from_bytes(self, ps):
        triangles = Triangles([Triangle((0, 1, 2))])
        b = triangles.to_bytes(ps)
        
        expected = bytearray()
        expected += struct.pack("<L", 3) # Nombre de point
        expected += struct.pack("<ff", 0.0, 0.0) # point 0
        expected += struct.pack("<ff", 1.0, 0.0) # point 1
        expected += struct.pack("<ff", 1.0, 1.0) # point 2

        expected += struct.pack("<L", 1) # Nombre de triangle
        expected += struct.pack("<LLL", 0, 1, 2) # Indices

        assert b == expected

        triangles2 = Triangles.from_bytes(b)
        assert len(triangles2) == 1
        assert triangles2.triangles[0].indices == (0, 1, 2)

    def test_triangles_from_bytes_invalid(self):
        with pytest.raises(ValueError):
            Triangles.from_bytes(b"\x00\x00")
