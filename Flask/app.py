from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
import secrets, bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]
auth_tokens = db["auth_tokens"]

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def render_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password)
        user = users.find_one({"username": username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            token = secrets.token_hex(16)
            hashed_token = bcrypt.hashpw(token.encode('utf-8'), bcrypt.gensalt())
            auth_tokens.insert_one({"username": username, "token": hashed_token})
            session['username'] = username
            response = jsonify({"message": "Login successful"})
            response.set_cookie("auth_token", token, httponly=True, max_age=3600)
            return response
        else:
            return jsonify({"error": "Invalid username or password"}), 401
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def render_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        print(username,password, confirm_password)
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400

        if users.find_one({"username": username}):
            return jsonify({"error": "Username already taken"}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert_one({"username": username, "password": hashed_password})
        return jsonify({"message": "User registered successfully"}), 201
        
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    response = redirect(url_for('home'))
    response.set_cookie('auth_token', '', expires=0)
    return response

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8080)
