from app import app
from app.models import User, Spiele, Partien
from flask import jsonify

@app.route('/api/users', methods=['GET'])
def get_users():
    data = User.to_collection()
    return jsonify(data)

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    data = User.query.get_or_404(id).to_dict()
    return jsonify(data)

@app.route('/api/spiele', methods=['GET'])
def get_spiele():
    data = Spiele.to_collection()
    return jsonify(data)

@app.route('/api/partien', methods=['GET'])
def get_partien():
    data = Partien.to_collection()
    return jsonify(data)