from flask import Flask, render_template, request, redirect, url_for, make_response
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from util.login import register
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]
tokens = db["tokens"]

def generate_token():
    return str(uuid.uuid4())


@app.route('/')
def redirect_to_login():
    return redirect(url_for('render_login'))

@app.route('/login', methods=['GET', 'POST'])
def render_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username':
        username})
        if user and Bcrypt.check_password_hash(user['password'], password.decode()):
            auth_token = generate_token()
            register(username, password)
            response = make_response(redirect(url_for('home')))
            expires = datetime.now() + timedelta(hours=1)
            response.set_cookie('auth_token', auth_token, expires=expires, httponly=True)
            return response
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/home')
def home():
    auth_token = request.cookies.get('auth_token')
    if auth_token:
        token = tokens.find_one({'token': Bcrypt.generate_pass_hash(auth_token).decode()})
        if token:
            username = token['username']
            return render_template('index.html', username=username)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def render_register():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            return render_template('register.html', error='Passwords do not match')
        
        if users.find_one({'username': username}):
            return render_template('register.html', error='Username already taken')
        
        register(username, Bcrypt.generate_password_hash(password1).decode())
        return redirect(url_for('render_login'))
    
    return render_template('register.html')


@app.route('/post-question', methods=['GET', 'POST'])
def post_question():
    if request.method == 'POST':
        question = request.form['question']
        answers = [request.form.get(f'answer{i}') for i in range(1, 5)]  # Collecting 4 answers
        correct_answer_index = request.form['correct_answer']  # Assuming this is the index (1-4) of the correct answer

        # Here, you would validate the input (e.g., at least 2 answers are provided) and save to your database

        pass  # Replace with your saving logic

    return render_template('post-question.html')


@app.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('render_login')))
    response.set_cookie('auth_token', '', expires=0, httponly=True)
    return response

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8000)