"""Module de tests pour la classe PointSet."""

import struct

import pytest

from pointset_manager.models.PointSet import Point, PointSet


class TestPointSet:
    """Classe de tests pour la classe PointSet."""
    
    def test_len_and_add(self):
        """Teste la longueur et l'ajout de points à un PointSet."""
        ps = PointSet([])
        assert len(ps) == 0

        ps.add_point(Point(1.0, 1.0))
        assert len(ps) == 1

    def test_add_point_invalid(self):
        """Teste l'ajout de points invalides à un PointSet."""
        ps = PointSet([])
        
        with pytest.raises(TypeError):
            ps.add_point("pas un point")
        
        with pytest.raises(TypeError):
            ps.add_point((1.0, 1.0))

    def test_pointset_to_bytes_and_from_bytes(self):
        """Teste la conversion en bytes et la reconversion d'un PointSet."""
        points = [Point(0.0, 0.0), Point(1.0, 1.0)]
        ps = PointSet(points)
        b = ps.to_bytes()
        assert len(b) == 4 + 2 * 8

        ps2 = PointSet.from_bytes(b)
        assert len(ps2) == 2
        assert ps2.points[0].x == pytest.approx(0.0)
        assert ps2.points[1].x == pytest.approx(1.0)

    def test_pointset_from_bytes_invalid(self):
        """Teste la conversion depuis des bytes invalides."""
        with pytest.raises(ValueError):
            PointSet.from_bytes(b"\x00\x00\x00")
        
        with pytest.raises(TypeError):
            PointSet.from_bytes(None)

        with pytest.raises(TypeError):
            PointSet.from_bytes("pas des bytes")
        
        with pytest.raises(ValueError):
            PointSet.from_bytes(b"")
        
        with pytest.raises(ValueError):
            b = struct.pack("<L", 2) + struct.pack("<ff", 1.0, 2.0)
            PointSet.from_bytes(b)
    
    def test_empty_pointset_to_bytes(self):
        """Teste la conversion en bytes d'un PointSet vide."""
        ps = PointSet([])

        with pytest.raises(ValueError):
            ps.to_bytes()
