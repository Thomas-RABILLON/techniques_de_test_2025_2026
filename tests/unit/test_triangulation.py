import pytest

from pointset_manager.models.PointSet import PointSet, Point
from triangulator.models.Triangles import Triangles, Triangle
from triangulator.core.triangulate import triangulate

class TestTriangulation:
    def test_triangulation_minimal(self):
        ps = PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)])
        exp_triangles = Triangles([Triangle((0, 1, 2))])
        
        triangles = triangulate(ps)
        assert len(triangles) == 1
        assert exp_triangles.triangles[0].indices == triangles.triangles[0].indices

    def test_not_enough_points(self):
        ps = PointSet([Point(0.0, 0.0), Point(1.0, 0.0)])

        with pytest.raises(ValueError):
            triangulate(ps)

    def test_colinear_points(self):
        ps = PointSet([Point(0.0, 0.0), Point(1.0, 1.0), Point(2.0, 2.0)])

        with pytest.raises(ValueError):
            triangulate(ps)
