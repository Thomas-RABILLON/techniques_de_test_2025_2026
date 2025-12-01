import time
import pytest

from pointset_manager.models.PointSet import PointSet, Point
from triangulator.core.triangulate import triangulate

@pytest.mark.performance
def test_triangulation_100_points():
    ps = PointSet([Point(i * 0.1, (i % 10) * 0.1) for i in range(100)])
    
    start = time.perf_counter()
    _ = triangulate(ps)
    duration = time.perf_counter() - start

    assert duration < 0.5


@pytest.mark.performance
def test_triangulation_1000_points():
    ps = PointSet([Point(i * 0.01, (i % 30) * 0.01) for i in range(1000)])
    
    start = time.perf_counter()
    _ = triangulate(ps)
    duration = time.perf_counter() - start
    
    assert duration < 2.0


@pytest.mark.performance
def test_triangulation_10000_points():
    ps = PointSet([Point(i * 0.001, (i % 50) * 0.001) for i in range(10000)])
    
    start = time.perf_counter()
    _ = triangulate(ps)
    
    duration = time.perf_counter() - start
    assert duration < 10.0
