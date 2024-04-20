from pymongo import MongoClient
from flask import jsonify
import bcrypt
import re,os  # Import regular expression module for pattern matching

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]

def validate_password(password):
    """Helper function to validate password requirements."""
    if len(password) < 8:
        return False, "Passwords must be at least 8 characters"
    if not re.search("[0-9]", password):
        return False, "Passwords must contain at least one number"
    if not re.search("[A-Z]", password):
        return False, "Passwords must contain one uppercase letter"
    if not re.search("[a-z]", password):
        return False, "Passwords must contain one lowercase letter"
    return True, ""

def validate_username(username):
    """Helper function to validate username requirements."""
    if not (5 <= len(username) <= 16):
        return False, "Username must be between 5 and 16 characters"
    if users.find_one({"username": username}):
        return False, "Username already taken"
    return True, ""

def register(username, password, confirm_password):
    if password != confirm_password:
        return "Passwords do not match", 400

    # Validate username
    valid_username, username_message = validate_username(username)
    if not valid_username:
        return username_message, 400

    # Validate password
    valid_password, password_message = validate_password(password)
    if not valid_password:
        return password_message, 400

    # If all validations pass, proceed to register the user
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users.insert_one({"username": username, "password": hashed_password})
    return "User registered successfully", 201



