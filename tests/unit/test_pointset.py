import pytest

from pointset_manager.models.PointSet import PointSet, Point

class TestPointSet:
    def test_len_and_add(self):
        ps = PointSet([])
        assert len(ps) == 0

        ps.add_point(Point(1.0, 1.0))
        assert len(ps) == 1

    def test_add_point_invalid(self):
        ps = PointSet([])
        
        with pytest.raises(ValueError):
            ps.add_point(Point(None, 1.0))
        
        with pytest.raises(ValueError):
            ps.add_point(Point(float("nan"), 1.0))

    def test_pointset_to_bytes_and_from_bytes(self):
        points = [Point(0.0, 0.0), Point(1.0, 1.0)]
        ps = PointSet(points)
        b = ps.to_bytes()
        assert len(b) == 4 + 2 * 8

        ps2 = PointSet.from_bytes(b)
        assert len(ps2) == 2
        assert ps2.points[0].x == pytest.approx(0.0)
        assert ps2.points[1].x == pytest.approx(1.0)

    def test_pointset_from_bytes_invalid(self):
        with pytest.raises(ValueError):
            PointSet.from_bytes(b"\x00\x00\x00")
