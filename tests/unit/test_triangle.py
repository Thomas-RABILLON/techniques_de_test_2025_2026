import struct
import pytest

from triangulator.models.Triangles import Triangle

class TestTriangle:
    def test_triangle_init_invalid(self):
        with pytest.raises(ValueError):
            Triangle((0, None, 1))

        with pytest.raises(ValueError):
            Triangle((0, 1))

    def test_triangle_to_bytes_valid(self):
        t = Triangle((0, 1, 2))
        b = t.to_bytes()
        assert len(b) == 12

        expected = struct.pack("<LLL", 0, 1, 2)
        assert b == expected

    def test_triangle_from_bytes_valid(self):
        b = struct.pack("<LLL", 5, 6, 7)
        t = Triangle.from_bytes(b)
        assert t.indices == (5, 6, 7)

    def test_triangle_from_bytes_invalid(self):
        with pytest.raises(ValueError):
            Triangle.from_bytes(b"\x00")
