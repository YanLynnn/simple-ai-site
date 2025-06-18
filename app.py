from flask import Flask, render_template, request, redirect, session, url_for
import json
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecret'

def load_users():
    with open('users.json') as f:
        return json.load(f)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user['username'] == username and check_password_hash(user['password'], password):
                session['username'] = username
                return redirect(url_for('home'))
        return 'Login failed!'
    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
