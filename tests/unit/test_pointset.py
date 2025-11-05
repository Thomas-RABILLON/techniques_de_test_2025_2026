import pytest

from pointset_manager.models.PointSet import PointSet, Point

class TestPointSet:
    @pytest.fixture
    def correct_point(self) -> Point:
        return Point(0.0, 0.0)
    
    @pytest.fixture
    def none_incorrect_point(self) -> Point:
        return Point(None, 0.0)
    
    @pytest.fixture
    def nan_incorrect_point(self) -> Point:
        return Point(0.0, 'a')
    
    @pytest.fixture
    def point_correct_bytes(self) -> str:
        return '00000000000000000000000000000000' \
                '00000000000000000000000000000000' \
    
    @pytest.fixture
    def point_incorrect_bytes(self) -> str:
        # Avec une coordonnée en moins
        return '00000000000000000000000000000000'

    @pytest.fixture
    def pointset_correct_bytes(self) -> str:
        return '00000000000000000000000000000011' \
                '00000000000000000000000000000000' \
                '00000000000000000000000000000000' \
                '00111111100000000000000000000000' \
                '00111111100000000000000000000000' \
                '00111111100000000000000000000000' \
                '00000000000000000000000000000000'
    
    @pytest.fixture
    def pointset_incorrect_bytes(self, pointset_correct_bytes: str) -> str:
        # Avec une byte en plus (pas la bonne longueur)
        return pointset_correct_bytes + '00000000'
    
    @pytest.fixture
    def correct_3_points_pointset(self) -> PointSet:
        return PointSet([Point(0.0, 0.0), Point(1.0, 1.0), Point(1.0, 0.0)])
    
    @pytest.fixture
    def none_incorrect_3_points_poinset(self) -> PointSet:
        return PointSet([Point(0.0, 0.0), Point(1.0, 1.0), Point(None, 0.0)])
    
    @pytest.fixture
    def nan_incorrect_3_points_pointset(self) -> PointSet:
        return PointSet([Point(0.0, 'a'), Point(1.0, 1.0), Point(1.0, 0.0)])

    @pytest.fixture
    def correct_0_points_pointset(self) -> PointSet:
        return PointSet([])
    
    def test_point_to_bytes(self, point_correct_bytes: str, correct_point: Point, none_incorrect_point: Point, nan_incorrect_point: Point):
        assert correct_point.to_bytes() == point_correct_bytes

        with pytest.raises(ValueError):
            none_incorrect_point.to_bytes()
            nan_incorrect_point.to_bytes()
    
    def test_point_from_bytes(self, point_correct_bytes: str, point_incorrect_bytes: str, correct_point: Point):
        assert Point.from_bytes(point_correct_bytes) == correct_point

        with pytest.raises(ValueError):
            Point.from_bytes(point_incorrect_bytes)
    
    def test_pointset_len(self, correct_3_points_pointset: PointSet, correct_0_points_pointset: PointSet):
        assert len(correct_3_points_pointset) == 3
        assert len(correct_0_points_pointset) == 0

        correct_0_points_pointset.addPoint(Point(0.0, 0.0))
        assert len(correct_0_points_pointset) == 1

    def test_pointset_to_bytes(self, pointset_correct_bytes: str, correct_3_points_pointset: PointSet, none_incorrect_3_points_poinset: PointSet, nan_incorrect_3_points_pointset: PointSet):
        assert correct_3_points_pointset.to_bytes() == pointset_correct_bytes

        with pytest.raises(ValueError):
            none_incorrect_3_points_poinset.to_bytes()
            nan_incorrect_3_points_pointset.to_bytes()
    
    def test_pointset_from_bytes(self, pointset_correct_bytes: str, pointset_incorrect_bytes: str, correct_3_points_pointset: PointSet):
        assert PointSet.from_bytes(pointset_correct_bytes) == correct_3_points_pointset

        with pytest.raises(ValueError):
            PointSet.from_bytes(pointset_incorrect_bytes)
