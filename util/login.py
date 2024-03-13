from pymongo import MongoClient
from flask import jsonify, request, session, redirect, url_for, make_response
import secrets, bcrypt

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]

def login(username, password):
    user = users.find_one({"username": username})
    if user:
        stored_password_hash = user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            token = secrets.token_hex(16)
            hashed_token = bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt())
            
            users.update_one({"username": username}, {"$set": {"auth_token": hashed_token}})
            
            return True, token
    return False, None

