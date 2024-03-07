from flask import Flask, render_template, request, redirect, url_for
from util.login import register

app = Flask(__name__)

@app.route('/')
def redirect_to_login():
    return redirect(url_for('render_login'))

@app.route('/login', methods=['GET', 'POST'])
def render_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register(username, password)
        
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def render_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register(username, password)
        
    return render_template('register.html')

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8000)
