"""Application Flask pour la gestion des PointSets et triangulation."""

from flask import Flask, jsonify, request

from pointset_manager.models.PointSet import PointSet
from triangulator.core.triangulate import Triangulator

app = Flask(__name__)

pointsets_store = {}
next_id = [1]

@app.route("/pointset", methods=["POST"])
def create_pointset():
    """Crée un nouveau PointSet à partir des données reçues.

    Returns:
        tuple: Réponse JSON avec l'ID du PointSet créé et statut 201,
               ou message d'erreur et statut 400.
    
    """
    data = request.data
    try:
        ps = PointSet.from_bytes(data)
    except (ValueError, TypeError):
        return "Erreur de données", 400
    
    ps_id = next_id[0]
    next_id[0] += 1

    pointsets_store[ps_id] = ps

    return jsonify({"PointSetID": ps_id}), 201

@app.route("/pointset/<pointset_id>", methods=["GET"])
def get_pointset(pointset_id):
    """Récupère un PointSet par son identifiant.

    Args:
        pointset_id (str): Identifiant du PointSet à récupérer.

    Returns:
        tuple: Données binaires du PointSet et statut 200,
               ou message d'erreur et statut approprié.
    
    """
    try:
        int_id = int(pointset_id)
    except ValueError:
        return "Identifiant invalide", 400

    ps = pointsets_store.get(int_id)

    if ps is None:
        return "Identifiant inexistant", 404
    return ps.to_bytes(), 200, {"Content-Type": "application/octet-stream"}

@app.route("/triangulation/<pointset_id>", methods=["GET"])
def get_triangulation(pointset_id):
    """Permet de calculer la triangulation d'un PointSet par son identifiant.

    Args:
        pointset_id (str): Identifiant du PointSet à trianguler.

    Returns:
        tuple: Données binaires de la triangulation et statut 200,
               ou message d'erreur et statut approprié.
    
    """
    # Utiliser l'endpoint /pointset/{pointset_id} pour récupérer le PointSet
    with app.test_client() as client:
        response = client.get(f"/pointset/{pointset_id}")
        
        if response.status_code != 200:
            return response.data, response.status_code
        
        try:
            ps = PointSet.from_bytes(response.data)
            triangles = Triangulator.triangulate(ps)
            return (
                triangles.to_bytes(), 
                200, 
                {"Content-Type": "application/octet-stream"}
            )
        except Exception:
            return "Erreur de triangulation", 500            


def create_app():
    """Crée et retourne l'application Flask.

    Returns:
        Flask: L'application Flask configurée.
    
    """
    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
