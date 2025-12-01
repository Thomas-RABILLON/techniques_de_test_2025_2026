import pytest

from client.app import create_app
from pointset_manager.models.PointSet import PointSet, Point

class TestTriangulator:
    @pytest.fixture
    def client(self):
        app = create_app()
        with app.test_client() as c:
            yield c

    def test_triangulation_success(self, client):
        pointset = PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)])
        
        rep_create = client.post("/pointset", data=pointset.to_bytes(), content_type="application/octet-stream")
        pointset_id = rep_create.get_json()["pointSetId"]

        rep = client.get(f"/triangulation/{pointset_id}")
        assert rep.status_code == 200
        
        data = rep.data
        assert len(data) > 0

    def test_triangulation_invalid_id(self, client):
        rep = client.get("/triangulation/invalid-id")
        assert rep.status_code in 404

    def test_triangulation_insufficient_points(self, client):
        pointset = PointSet([Point(0.0, 0.0), Point(1.0, 0.0)])
        
        rep_create = client.post("/pointset", data=pointset.to_bytes(), content_type="application/octet-stream")
        pointset_id = rep_create.get_json()["pointSetId"]

        rep = client.get(f"/triangulation/{pointset_id}")
        assert rep.status_code == 500
