from flask import Flask, render_template, request, redirect, url_for
from util.login import register

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def render_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register(username, password)
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def render_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register(username, password)
        
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

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8080)
