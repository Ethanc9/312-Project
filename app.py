from flask import Flask, render_template, request, redirect, url_for, session, make_response
from util.register import register

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient("mongo")
db = client["cse312"]
users = db["users"]


@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return render_template('index.html')

@app.route('/post-question', methods=['GET', 'POST'])
def post_question():
    return render_template('post-question.html')

@app.route('/login', methods=['GET', 'POST'])
def render_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return login(username, password)
    return render_template('login.html')


# Flask app setup and other routes remain unchanged

@app.route('/register', methods=['GET', 'POST'])
def render_register():
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
    response = redirect(url_for('render_login'))
    response.set_cookie('auth_token', '', expires=0)
    return response

@app.after_request
def add_header(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=8080, host = '0.0.0.0')

