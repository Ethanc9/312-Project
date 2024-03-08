from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from flask import jsonify

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]

def register(username, password, confirm_password):
    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    if users.find_one({"username": username}):
        return jsonify({"error": "Username already taken"}), 400

    hashed_password = generate_password_hash(password)
    users.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "User registered successfully"}), 201