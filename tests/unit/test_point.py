"""Module de tests pour la classe Point."""

import struct

import pytest

from pointset_manager.models.Point import Point


class TestPoint:
    """Classe de tests pour la classe Point."""
    
    def test_point_invalid_init(self):
        """Teste l'initialisation invalide d'un point."""
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
        """Teste la conversion en bytes d'un point valide."""
        p = Point(0.0, 1.0)
        b = p.to_bytes()
        assert len(b) == 8
        
        expected = struct.pack("<ff", 0.0, 1.0)
        assert b == expected

    def test_point_from_bytes_valid(self):
        """Teste la conversion depuis des bytes d'un point valide."""
        b = struct.pack("<ff", 1.0, 0.0)
        p = Point.from_bytes(b)
        
        assert p.x == pytest.approx(1.0)
        assert p.y == pytest.approx(0.0)

    def test_point_from_bytes_invalid_source_len(self):
        """Teste la conversion depuis des bytes avec longueur invalide."""
        with pytest.raises(ValueError):
            Point.from_bytes(b"\x00\x01")
    
    def test_point_from_bytes_invalid_length(self):
        """Teste la conversion depuis des bytes de longueur incorrecte."""
        with pytest.raises(ValueError):
            Point.from_bytes(b"\x00\x01\x02")
    
    def test_point_from_bytes_invalid_type(self):
        """Teste la conversion depuis un type invalide."""
        with pytest.raises(TypeError):
            Point.from_bytes("pas des bytes")
