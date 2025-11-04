import pytest

from pointset_manager.models.PointSet import PointSet, Point

class TestPointSet:
    correct_bytes = '00000000000000000000000000000011' \
                    '00000000000000000000000000000000' \
                    '00000000000000000000000000000000' \
                    '00111111100000000000000000000000' \
                    '00111111100000000000000000000000' \
                    '00111111100000000000000000000000' \
                    '00000000000000000000000000000000'

    @pytest.fixture
    def init_point(self) -> list:
        return [Point(0.0, 0.0), Point(1.0, 1.0), Point(1.0, 0.0)]
    
    @pytest.fixture
    def init_pointset(self, init_point) -> PointSet:
        return PointSet(init_point)
    
    def test_pointset_len(self, init_pointset):
        assert len(init_pointset) == 3

    def test_to_bytes(self, init_pointset):
        assert init_pointset.to_bytes() == self.correct_bytes
    
    def test_from_bytes(self, init_pointset):
        assert PointSet.from_bytes(self.correct_bytes) == init_pointset
