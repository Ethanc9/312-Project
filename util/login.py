from pymongo import MongoClient
from flask import jsonify, request, session, redirect, url_for
import secrets, bcrypt

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]

def login(username, password):
    user = users.find_one({"username": username})
    if user:
        # The stored password hash is retrieved from the user document.
        stored_password_hash = user["password"]
        
        # The password provided by the user is encoded and compared with the stored hash.
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            token = secrets.token_hex(16)
            hashed_token = bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt())
            
            # Update the user document to include the hashed auth_token
            users.update_one({"username": username}, {"$set": {"auth_token": hashed_token}})
            session['username'] = username  # Store username in session for easy retrieval
            
            # Redirect to the home page and set the auth_token cookie
            response = redirect(url_for('home_route'))
            ten_years_in_seconds = 10 * 365 * 24 * 60 * 60
            response.set_cookie("auth_token", token, httponly=True, max_age=ten_years_in_seconds)
            return response
        else:
            # If the password does not match, redirect to the login page
            return redirect(url_for('login_route'))
    else:
        # If the user does not exist, also redirect to the login page
        return redirect(url_for('login_route'))