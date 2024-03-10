from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from util.register import register
from util.login import login
from pymongo import MongoClient
from bson.objectid import ObjectId  # For generating unique IDs
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]
questions = db["questions"]

@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', user_name=session['username'])
    return render_template('index.html')

@app.route('/post-question', methods=['GET', 'POST'])
def post_question():
    if request.method == 'POST':
        data = request.json
        user_id = session.get('user_id')  # Assuming session management includes user_id
        question_text = data['question']
        answers = data['answers']
        
        # Insert the question and answers into the database
        question_id = insert_question(user_id, question_text, answers)
        
        return jsonify({'success': True, 'redirect': url_for('home')})
    return render_template('post-question.html')

def insert_question(user_id, question_text, answers):
    """
    Inserts a question along with its answers into the database.

    Parameters:
    - user_id: The ID of the user posting the question.
    - question_text: The text of the question.
    - answers: A list of answers to the question.
    """
    question_id = ObjectId()  # Generates a unique ID for the question
    question_document = {
        "_id": question_id,
        "user_id": user_id,
        "question_text": question_text,
        "answers": answers,
        "posted_at": datetime.datetime.utcnow()  # Stores the current time
    }
    questions.insert_one(question_document)
    return question_id

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return login(username, password)
    return render_template('login.html')


# Flask app setup and other routes remain unchanged

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        message, status_code = register(username, password, confirm_password)
        
        if status_code == 201:
            response = make_response(redirect(url_for('render_login')))
            response.set_cookie('registration_success', 'true', max_age=10) 
            return response
        else:
            return render_template('register.html', error=message)
    else:
        registration_success = request.cookies.get('registration_success')
        if registration_success:
            alert_script = "<script>alert('User registered successfully. Please login.');</script>"
        else:
            alert_script = ""
        return render_template('register.html', alert_script=alert_script)

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
    app.run(debug=True, port=8080, host = '0.0.0.0')

