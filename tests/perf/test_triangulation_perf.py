"""Module de tests de performance pour la triangulation."""

import random
import time

import pytest

from pointset_manager.models.PointSet import Point, PointSet
from triangulator.core.triangulate import Triangulator


@pytest.mark.perf
def test_triangulation_10_points():
    """Teste les performances de triangulation avec 10 points."""
    total_duration = 0
    for _ in range(1000):
        ps = PointSet([
            Point(random.uniform(0, 10), random.uniform(0, 10)) 
            for _ in range(10)
        ])
        start = time.perf_counter()
        Triangulator.triangulate(ps)
        duration = time.perf_counter() - start
        total_duration += duration

    mean_duration = total_duration / 1000
    assert mean_duration < 0.2

@pytest.mark.performance
def test_triangulation_100_points():
    """Teste les performances de triangulation avec 100 points."""
    total_duration = 0
    for _ in range(100):
        ps = PointSet([
            Point(random.uniform(0, 10), random.uniform(0, 10)) 
            for _ in range(100)
        ])
        start = time.perf_counter()
        Triangulator.triangulate(ps)
        duration = time.perf_counter() - start
        total_duration += duration

    mean_duration = total_duration / 100
    assert mean_duration < 0.5


@pytest.mark.perf
def test_triangulation_1000_points():
    """Teste les performances de triangulation avec 1000 points."""
    total_duration = 0
    for _ in range(10):
        ps = PointSet([
            Point(random.uniform(0, 100), random.uniform(0, 100)) 
            for _ in range(1000)
        ])
        start = time.perf_counter()
        Triangulator.triangulate(ps)
        duration = time.perf_counter() - start
        total_duration += duration
    
    mean_duration = total_duration / 10
    assert mean_duration < 10.0

@pytest.mark.perf
def test_triangulation_10000_points():
    """Teste les performances de triangulation avec 10000 points."""
    ps = PointSet([
        Point(random.uniform(0, 1000), random.uniform(0, 1000)) 
        for _ in range(10000)
    ])

    start = time.perf_counter()
    Triangulator.triangulate(ps)
    duration = time.perf_counter() - start
    
    assert duration < 180.0
