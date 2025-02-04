import logging
import os
from flask import Flask, jsonify
from pymongo import MongoClient
from bson import ObjectId
import json

app = Flask(__name__)

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017')
client = MongoClient(MONGO_URI)
db = client['db']
collection_users = db['users']
collection_clothes = db['clothes']

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

app.json_encoder = JSONEncoder

@app.route("/user/<int:user_id>/products/", methods=["GET"])
def index(user_id):
    user = collection_users.find_one({"node.userId": user_id})
    if not user:
        return {"error": "User not found"}, 404

    # Get user's purchased clothes
    clothes = user['node']['purchasedClothes']

    # Get friends' purchased clothes
    relationships = user['outgoing_relations']
    for relationship in relationships:
        friend = collection_users.find_one({"node.userId": relationship["userId"]})
        if friend:
            clothes += friend['node']['purchasedClothes']

    # Convert ObjectId to string in the user document
    user['_id'] = str(user['_id'])

    clothes_data = []

    for cloth in clothes:
        cloth_data = collection_clothes.find_one({"clothesID": cloth})
        if cloth_data:
            cloth_data['_id'] = str(cloth_data['_id'])
            clothes_data.append(cloth_data)

    return jsonify(clothes_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)