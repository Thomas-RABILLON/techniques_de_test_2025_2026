import struct
import pytest

from triangulator.models.Triangles import Triangles, Triangle
from pointset_manager.models.PointSet import PointSet, Point

class TestTriangles:
    @pytest.fixture
    def ps(self) -> PointSet:
        return PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(1.0, 1.0), Point(0.0, 1.0)])

    def test_triangles_init_and_len(self, ps: PointSet):
        t = Triangles([Triangle((0, 1, 2))], ps)
        assert len(t) == 1
    
    def test_pointset_type_check(self):
        with pytest.raises(TypeError):
            Triangles([], "pointset")
    
    def test_add_triangle(self, ps):
        t = Triangles([], ps)
        t.add_triangles(Triangle((0, 1, 2)))

        assert t.triangles[0].indices == (0, 1, 2)

    def test_add_triangle_type_check(self, ps):
        t = Triangles([], ps)

        with pytest.raises(TypeError):
            t.add_triangles("bad")

    def test_triangles_to_bytes_and_from_bytes(self, ps: PointSet):
        triangles = Triangles([Triangle((0, 1, 2))], ps)
        b = triangles.to_bytes()
        
        expected = ps.to_bytes()

        expected += struct.pack("<L", 1)
        expected += struct.pack("<LLL", 0, 1, 2)

        assert b == expected

        triangles2 = Triangles.from_bytes(b)
        assert len(triangles2) == 1
        assert triangles2.triangles[0].indices == (0, 1, 2)
    
    def test_multiple_triangles_to_bytes_and_from_bytes(self, ps):
        triangles = Triangles([Triangle((0, 1, 2)), Triangle((0, 2, 3))], ps)
        b = triangles.to_bytes()

        expected = ps.to_bytes()
        expected += struct.pack("<L", 2)
        expected += struct.pack("<LLL", 0, 1, 2)
        expected += struct.pack("<LLL", 0, 2, 3)

        assert b == expected

        triangles2 = Triangles.from_bytes(b)
        assert len(triangles2) == 2
        assert triangles2.triangles[0].indices == (0, 1, 2)
        assert triangles2.triangles[1].indices == (0, 2, 3)
    
    def test_empty_triangles_to_bytes(self, ps):
        t = Triangles([], ps)

        with pytest.raises(ValueError):
            t.to_bytes()
    
    def test_from_bytes_bad_nb_triangle(self, ps):
        triangles = Triangles([Triangle((0, 1, 2))], ps)
        b = triangles.to_bytes()

        bad = bytearray(b)
        bad[len(ps.to_bytes())] = 2

        with pytest.raises(ValueError):
            Triangles.from_bytes(bytes(bad))
    
    def test_from_bytes_cut_source(self, ps):
        triangles = Triangles([Triangle((0, 1, 2))], ps)
        b = triangles.to_bytes()

        cut_source = b[:-4]

        with pytest.raises(ValueError):
            Triangles.from_bytes(cut_source)

    def test_triangles_from_bytes_invalid(self):
        with pytest.raises(ValueError):
            Triangles.from_bytes(b"\x00\x00")
    
    def test_from_bytes_invalid_type(self):
        with pytest.raises(TypeError):
            Triangles.from_bytes("pas des bytes")
