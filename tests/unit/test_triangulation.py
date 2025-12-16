"""Module de tests pour la classe Triangulator."""

import pytest

from pointset_manager.models.PointSet import Point, PointSet
from triangulator.core.triangulate import Triangulator
from triangulator.models.Triangles import Triangle, Triangles


class TestTriangulation:
    """Classe de tests pour la triangulation."""
    
    def test_triangulation_minimal(self):
        """Teste la triangulation minimale avec 3 points."""
        ps = PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)])
        exp_triangles = Triangles([Triangle((0, 1, 2))], ps)
        
        triangles = Triangulator.triangulate(ps)
        assert len(triangles) == 1
        assert exp_triangles.triangles[0].indices == triangles.triangles[0].indices

    def test_not_enough_points(self):
        """Teste la triangulation avec moins de 3 points."""
        ps = PointSet([Point(0.0, 0.0), Point(1.0, 0.0)])

        with pytest.raises(ValueError):
            Triangulator.triangulate(ps)

    def test_colinear_points(self):
        """Permet de tester la colinéarité des points."""
        ps = PointSet([Point(0.0, 0.0), Point(1.0, 1.0), Point(2.0, 2.0)])

        with pytest.raises(ValueError):
            Triangulator.triangulate(ps)
    
    def test_croisement(self):
        """Permet de tester le croisement des triangles."""
        ps = PointSet([
            Point(0.0, 0.0),
            Point(1.0, 0.0),
            Point(0.0, 1.0),
            Point(1.0, 1.0)
            ])
        triangles = Triangulator.triangulate(ps)
        assert len(triangles) == 2

        # Si il n'y a que 2 triangle, les 2 ne peuvent avoir que 2 points en commun
        tr0 = triangles.triangles[0]
        tr1 = triangles.triangles[1]
        
        count = 0
        for i in tr0.indices:
            if i in tr1.indices:
                count += 1
        assert count == 2
