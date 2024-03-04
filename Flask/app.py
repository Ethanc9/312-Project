from flask import Flask, render_template, request
from util.login import register

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def render_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register(username, password)
         

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
