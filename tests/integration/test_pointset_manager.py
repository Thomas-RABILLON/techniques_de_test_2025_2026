import pytest

from client.app import create_app
from pointset_manager.models.PointSet import PointSet, Point

class TestPointSetManager:
    @pytest.fixture
    def client(self):
        app = create_app()
        with app.test_client() as c:
            yield c

    def test_create_pointset_success(self, client):
        pointset = PointSet([Point(0.0, 0.0), Point(1.0, 1.0)])
        
        rep = client.post("/pointset", data=pointset.to_bytes(), content_type="application/octet-stream")
        assert rep.status_code == 201
        
        data = rep.get_json()
        assert "PointSetID" in data

    def test_create_pointset_invalid_bytes(self, client):
        rep = client.post("/pointset", data=b"\x00\x01", content_type="application/octet-stream")
        assert rep.status_code == 400

    def test_get_pointset_success(self, client):
        pointset = PointSet([Point(0.0, 0.0), Point(1.0, 1.0)])
        b = pointset.to_bytes()

        rep_create = client.post("/pointset", data=b, content_type="application/octet-stream")
        pointset_id = rep_create.get_json()["PointSetId"]

        rep_get = client.get(f"/pointset/{pointset_id}")
        assert rep_get.status_code == 200
        assert rep_get.data == b

    def test_get_pointset_not_found(self, client):
        rep = client.get("/pointset/invalidId")
        assert rep.status_code == 404
