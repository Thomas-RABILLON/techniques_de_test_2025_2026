"""Module de tests pour la classe Triangles."""

import struct

import pytest

from pointset_manager.models.PointSet import Point, PointSet
from triangulator.models.Triangles import Triangle, Triangles


class TestTriangles:
    """Classe de tests pour la classe Triangles."""
    
    @pytest.fixture
    def ps(self) -> PointSet:
        """Fixture fournissant un PointSet avec 4 points formant un carré."""
        return PointSet([
            Point(0.0, 0.0),
            Point(1.0, 0.0),
            Point(1.0, 1.0),
            Point(0.0, 1.0)
        ])

    def test_triangles_init_and_len(self, ps: PointSet):
        """Teste l'initialisation et la longueur d'un ensemble de triangles."""
        t = Triangles([Triangle((0, 1, 2))], ps)
        assert len(t) == 1
    
    def test_pointset_type_check(self):
        """Teste la vérification du type du PointSet."""
        with pytest.raises(TypeError):
            Triangles([], "pointset")
    
    def test_add_triangle(self, ps):
        """Teste l'ajout d'un triangle à l'ensemble."""
        t = Triangles([], ps)
        t.add_triangles(Triangle((0, 1, 2)))

        assert t.triangles[0].indices == (0, 1, 2)

    def test_add_triangle_type_check(self, ps):
        """Teste la vérification du type lors de l'ajout d'un triangle."""
        t = Triangles([], ps)

        with pytest.raises(TypeError):
            t.add_triangles("bad")

    def test_triangles_to_bytes_and_from_bytes(self, ps: PointSet):
        """Teste la conversion en bytes et la reconversion."""
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
        """Teste la conversion en bytes et la reconversion de plusieurs triangles."""
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
        """Teste la conversion en bytes d'un ensemble de triangles vide."""
        t = Triangles([], ps)

        with pytest.raises(ValueError):
            t.to_bytes()
    
    def test_from_bytes_bad_nb_triangle(self, ps):
        """Teste la conversion depuis des bytes avec un nombre de triangles invalide."""
        triangles = Triangles([Triangle((0, 1, 2))], ps)
        b = triangles.to_bytes()

        bad = bytearray(b)
        bad[len(ps.to_bytes())] = 2

        with pytest.raises(ValueError):
            Triangles.from_bytes(bytes(bad))
    
    def test_from_bytes_cut_source(self, ps):
        """Teste la conversion depuis des bytes tronqués."""
        triangles = Triangles([Triangle((0, 1, 2))], ps)
        b = triangles.to_bytes()

        cut_source = b[:-4]

        with pytest.raises(ValueError):
            Triangles.from_bytes(cut_source)

    def test_triangles_from_bytes_invalid(self):
        """Teste la conversion depuis des bytes invalides."""
        with pytest.raises(ValueError):
            Triangles.from_bytes(b"\x00\x00")
    
    def test_from_bytes_invalid_type(self):
        """Teste la conversion depuis un type invalide."""
        with pytest.raises(TypeError):
            Triangles.from_bytes("pas des bytes")
