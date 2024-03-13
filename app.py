from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify
from util.questions import *
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
submissions = db["submissions"]

@app.route('/')
def home_route():
    if 'username' in session:
        return render_template('index.html', user_name=session['username'])
    return render_template('index.html')

@app.route('/answer-question', methods=['GET', 'POST'])
def answer_question():
    questions_data = output_questions()
    return render_template('answer.html', questions=questions_data)

@app.route('/post-question', methods=['GET', 'POST'])
def post_question():
    if request.method == 'POST':
        data = request.json
        print(data)
        username = session.get('username')
        question = data['question']
        answers = data['answers']
        correct_answer = int(data['correctAnswer'])  # Convert to int for safety
        # Validate the right_answer index
        if correct_answer >= len(answers):
            return jsonify({'success': False, 'error': 'correct_answer correct answer selection'}), 400
        insert_question(username, question, answers, correct_answer)
        return jsonify({'success': True, 'redirect': url_for('home_route')})
    return render_template('post-question.html')

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user, status_code = login(username, password)
        if status_code == 200:
            session['username'] = user['username']
            response = make_response(redirect(url_for('home_route')))
            response.set_cookie('authToken', 'true', max_age=3600)
            return response
    return render_template('login.html')


# Flask app setup and other routes remain unchanged

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        message, status_code = register(username, password, confirm_password)
        
        if status_code == 201:
            response = make_response(redirect(url_for('login_route')))
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
def logout_route():
    session.pop('username', None)
    response = redirect(url_for('home_route'))
    response.set_cookie('auth_token', '', expires=0)
    return response

@app.route('/validate-answer', methods=['POST'])
def validate_answer_route():
    data = request.json
    username = session.get('username')  # Assuming the user's username is stored in the session
    question_id = data['questionId']
    answer_index = data['answerIndex']
    
    # Call the validate_answer function from util/questions.py
    result = validate_answer(username, question_id, answer_index)
    
    if "isCorrect" in result:
        return jsonify(result)
    else:
        return jsonify(result), 404

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8080, host = '0.0.0.0')

