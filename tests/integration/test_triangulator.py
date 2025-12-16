"""Module de tests d'intégration pour Triangulator."""

import pytest

from client.app import create_app
from pointset_manager.models.PointSet import Point, PointSet


class TestTriangulator:
    """Classe de tests d'intégration pour Triangulator."""
    
    @pytest.fixture
    def serveur(self):
        """Fixture pour le client de test de l'application."""
        app = create_app()
        with app.test_client() as c:
            yield c

    def test_triangulation_success(self, serveur):
        """Teste la triangulation réussie."""
        pointset = PointSet([Point(0.0, 0.0), Point(1.0, 0.0), Point(0.0, 1.0)])
        
        rep_create = serveur.post(
            "/pointset", 
            data=pointset.to_bytes(), 
            content_type="application/octet-stream"
        )
        pointset_id = rep_create.get_json()["PointSetID"]

        rep = serveur.get(f"/triangulation/{pointset_id}")
        assert rep.status_code == 200
        
        data = rep.data
        assert len(data) > 0

    def test_triangulation_invalid_id(self, serveur):
        """Teste la triangulation avec un ID invalide."""
        rep = serveur.get("/triangulation/1234567890")
        assert rep.status_code == 404

        rep = serveur.get("/triangulation/invalid-id")
        assert rep.status_code == 400

    def test_triangulation_insufficient_points(self, serveur):
        """Teste la triangulation avec un nombre de points insuffisant."""
        pointset = PointSet([Point(0.0, 0.0), Point(1.0, 0.0)])
        
        rep_create = serveur.post(
            "/pointset", 
            data=pointset.to_bytes(), 
            content_type="application/octet-stream"
        )
        pointset_id = rep_create.get_json()["PointSetID"]

        rep = serveur.get(f"/triangulation/{pointset_id}")
        assert rep.status_code == 500
