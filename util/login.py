from pymongo import MongoClient
from werkzeug.security import check_password_hash
from flask import jsonify, request, session
import secrets

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]
auth_tokens = db["auth_tokens"]

def login(username, password):
    user = users.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        token = secrets.token_hex(16)
        hashed_token = generate_password_hash(token)
        auth_tokens.insert_one({"username": username, "token": hashed_token})
        session['username'] = username  # Store username in session for easy retrieval
        response = jsonify({"message": "Login successful"})
        response.set_cookie("auth_token", token, httponly=True, max_age=3600)
        return response
    else:
        return jsonify({"error": "Invalid username or password"}), 401