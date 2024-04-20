from flask import Flask, render_template, request, redirect, url_for, session, make_response, jsonify, current_app, send_from_directory
import os
from markupsafe import escape
from util.questions import *
from util.register import *
from util.login import *
from pymongo import MongoClient
from bson.objectid import ObjectId  # For generating unique IDs
from flask_socketio import SocketIO, send, emit
import json
import uuid
import base64


app = Flask(__name__)
app.secret_key = 'your_secret_key'
socketio = SocketIO(app)

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]
questions = db["questions"]
submissions = db["submissions"]

UPLOAD_FOLDER = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_unique_filename(filename):
    # Extract the file extension from the image data
    ext = filename.split('/')[1]
    # Generate a unique filename using UUID
    unique_filename = str(uuid.uuid4()) + '.'+ ext
    return unique_filename

def allowed_file(filename):
    return filename.split('/')[1] in ALLOWED_EXTENSIONS

def save_image(image_data, filename):
    # Define the directory where you want to save the images
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # Create the directory if it doesn't exist
    os.makedirs(upload_folder, exist_ok=True)
    
    # Generate a unique filename for the image
    filename = generate_unique_filename(filename)
    
    # Combine the directory and filename to get the full path
    image_path = os.path.join(upload_folder, filename)
    
    # Save the image data to the specified path
    with open(image_path, 'wb') as f:
        f.write(image_data)
    
    return image_path

@socketio.on('connect')
def ws_connect():
    print('connected')

@socketio.on('message')
def ws_sendquestion(msg):
    print('questions upated')
    questions_data = output_questions()
    for i in questions_data:
        del i['posted_at']
    questions_data = json.dumps(questions_data[len(questions_data)-1])
    print(questions_data)
    emit('update_question', questions_data, broadcast=True)

@app.route('/', methods=['GET', 'POST'])
def home_route():
    user_name = None
    if 'auth_token' in request.cookies:
        user_name = get_username_from_token(request.cookies['auth_token'])
    return render_template('index.html', user_name=user_name)


@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'js'), filename)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), filename)


@app.route('/answer-question', methods=['GET', 'POST'])
def answer_question():
    questions_data = output_questions()
    return render_template('answer.html', questions=questions_data)

@app.route('/post-question', methods=['GET', 'POST'])
def post_question():
    if request.method == 'POST':
        username = session.get('username')
        if not username:
            # Redirect to login if the user is not logged in
            return redirect(url_for('login_route'))

        data = request.json
        question = escape(data['question'])  # HTML escape the question text
        answers = [escape(answer) for answer in data['answers']]  # Optionally escape answers too
        correct_answer = data['correctAnswer']

        if correct_answer >= len(answers):
            # Handle error: correct answer index out of range
            return "Error: Correct answer index out of range.", 400
        
        image_path = None
        if 'image' in data:
            image_data = data['image']
            parts = image_data.split(';base64,')
            if len(parts) == 2:
                data_type, base64_str = parts
                # Decode the base64 string
                image_data = base64.b64decode(base64_str)
                filename = data_type.split(':')[1]
                if allowed_file(filename):
                    print("HELLOOO")
                    image_path = save_image(image_data, filename)

        insert_question(username, question, answers, correct_answer, image_path)
        return redirect(url_for('home_route'))
    return render_template('post-question.html')


@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = escape(request.form['username'])
        password = escape(request.form['password'])
        authenticated, token = login(username, password)
        if authenticated:
            print("authenticated")
            # Authentication successful, set session and cookie
            session['username'] = username
            response = make_response(redirect(url_for('home_route')))
            ten_years_in_seconds = 10 * 365 * 24 * 60 * 60
            response.set_cookie("auth_token", token, httponly=True, max_age=ten_years_in_seconds)
            return response
        else:
            print("Enter Login")
            # Authentication failed, redirect to the login page
            return redirect(url_for('login_route'))
    else:
        print("Enter Login1")
        # Handle GET request by rendering the login form
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
    #socketio.run(app, allow_unsafe_werkzeug=True, port=8080, host = '0.0.0.0')