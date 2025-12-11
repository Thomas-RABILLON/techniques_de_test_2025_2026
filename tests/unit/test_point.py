import struct
import pytest

from pointset_manager.models.Point import Point

class TestPoint:    
    def test_point_invalid_init(self):
        with pytest.raises(TypeError):
            Point(None, 0.0)

        with pytest.raises(TypeError):
            Point(0.0, None)

        with pytest.raises(ValueError):
            Point(float("nan"), 1.0)
        
        with pytest.raises(ValueError):
            Point(0.0, float("nan"))

        with pytest.raises(ValueError):
            Point(float("inf"), 1.0)
        
        with pytest.raises(ValueError):
            Point(0.0, float("inf"))
        
        with pytest.raises(ValueError):
            Point(float("-inf"), 1.0)
        
        with pytest.raises(ValueError):
            Point(0.0, float("-inf"))

    def test_point_to_bytes_valid(self):
        p = Point(0.0, 1.0)
        b = p.to_bytes()
        assert len(b) == 8
        
        expected = struct.pack("<ff", 0.0, 1.0)
        assert b == expected

    def test_point_from_bytes_valid(self):
        b = struct.pack("<ff", 1.0, 0.0)
        p = Point.from_bytes(b)
        
        assert p.x == pytest.approx(1.0)
        assert p.y == pytest.approx(0.0)

    def test_point_from_bytes_invalid_source_len(self):
        with pytest.raises(ValueError):
            Point.from_bytes(b"\x00\x01")
    
    def test_point_from_bytes_invalid_length(self):
        with pytest.raises(ValueError):
            Point.from_bytes(b"\x00\x01\x02")
    
    def test_point_from_bytes_invalid_type(self):
        with pytest.raises(TypeError):
            Point.from_bytes("pas des bytes")
