from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print("Username:", username)
        print("Password:", password)

        return "Login Successful" 

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
