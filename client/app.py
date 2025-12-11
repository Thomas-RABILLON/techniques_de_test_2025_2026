from flask import Flask, request, jsonify, abort

from pointset_manager.models.PointSet import PointSet

app = Flask(__name__)

pointsets_store = {}
next_id = [1]

@app.route("/pointset", methods=["POST"])
def create_pointset():
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
    try:
        int_id = int(pointset_id)
    except:
        return "Identifiant invalide", 404

    ps = pointsets_store.get(int_id)

    if ps is None:
        return "Identifiant inexistant", 404
    return ps.to_bytes(), 200, {"Content-Type": "application/octet-stream"}

def create_app():
    return app

if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000)
