"""Module de tests pour la classe Triangle."""

import struct

import pytest

from pointset_manager.models.Point import Point
from pointset_manager.models.PointSet import PointSet
from triangulator.models.Triangles import Triangle


class TestTriangle:
    """Classe de tests pour la classe Triangle."""
    
    @pytest.fixture
    def pointset_3_points(self) -> PointSet:
        """Fixture fournissant un PointSet avec 3 points."""
        return PointSet([Point(0.0, 0.0), Point(1.0, 1.0), Point(2.0, 2.0)])
    
    @pytest.fixture
    def pointset_1_point(self) -> PointSet:
        """Fixture fournissant un PointSet avec 1 point."""
        return PointSet([Point(0.0, 0.0)])

    def test_triangle_init_invalid(self):
        """Teste l'initialisation invalide d'un triangle."""
        with pytest.raises(TypeError):
            Triangle((0, None, 1))

        with pytest.raises(ValueError):
            Triangle((0, 1))
        
        with pytest.raises(ValueError):
            Triangle((0, 1, 2, 3))

    def test_triangle_to_bytes_valid(self):
        """Teste la conversion valide d'un triangle en bytes."""
        t = Triangle((0, 1, 2))
        b = t.to_bytes()
        assert len(b) == 12

        expected = struct.pack("<LLL", 0, 1, 2)
        assert b == expected

    def test_from_bytes_valid(self, pointset_3_points: PointSet):
        """Teste la conversion valide de bytes en triangle."""
        b = struct.pack("<LLL", 2, 1, 0)

        t = Triangle.from_bytes(b, pointset_3_points)
        assert t.indices == (2, 1, 0)
    
    def test_from_bytes_invalied_index(self, pointset_3_points: PointSet):
        """Teste la conversion de bytes avec des indices invalides."""
        b = struct.pack("<LLL", 0, 5, 1)
        with pytest.raises(IndexError):
            Triangle.from_bytes(b, pointset_3_points)

    def test_from_bytes_invalid_source_len(self, pointset_1_point: PointSet):
        """Teste la conversion de bytes avec une source trop courte."""
        with pytest.raises(ValueError):
            Triangle.from_bytes(b"\x00", pointset_1_point)
    
    def test_from_bytes_invalid_len(self, pointset_1_point: PointSet):
        """Teste la conversion de bytes avec une longueur invalide."""
        with pytest.raises(ValueError):
            Triangle.from_bytes(b"\x00\x00\x00", pointset_1_point)
    
    def test_from_bytes_invalid_source_type(self, pointset_1_point: PointSet):
        """Teste la conversion avec un type de source invalide."""
        with pytest.raises(TypeError):
            Triangle.from_bytes("pas des bytes", pointset_1_point)

    def test_from_bytes_pointset_none(self):
        """Teste la conversion avec un PointSet None."""
        b = struct.pack("<LLL", 0, 1, 2)

        with pytest.raises(ValueError):
            Triangle.from_bytes(b, None)

