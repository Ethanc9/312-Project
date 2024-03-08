from pymongo import MongoClient
from flask import jsonify
import bcrypt

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]

def register(username, password, confirm_password):
    if password != confirm_password:
        return "Passwords do not match", 400

    if users.find_one({"username": username}):
        return "Username already taken", 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users.insert_one({"username": username, "password": hashed_password})
    return "User registered successfully", 201