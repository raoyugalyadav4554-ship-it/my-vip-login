from flask import Flask, render_template, request, session, redirect, url_for
import random
import re
import json
import os

app = Flask(__name__)
app.secret_key = "permanent_vip_key_2026"

# Database file ka naam
DB_FILE = "users_db.json"

# Data load karne ka function
def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Data save karne ka function
def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def is_strong_password(psw):
    return (len(psw) >= 8 and re.search(r"[A-Z]", psw) and re.search(r"[a-z]", psw) and 
            re.search(r"\d", psw) and re.search(r"[@$!%*?&#]", psw))

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login_page')
def login_page():
    captcha_text = "".join(random.choice("23456789ABC") for _ in range(4))
    session['captcha'] = captcha_text
    return render_template('login.html', captcha=captcha_text)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        phone = request.form.get('phone')
        pw = request.form.get('password')
        conf_pw = request.form.get('confirm_password')
        invite = request.form.get('invite_code')

        users = load_data()

        if invite != "LDNE19" or pw != conf_pw or not is_strong_password(pw):
            return "<h1>❌ Error: Check Password Match or Invite Code!</h1><a href='/signup'>Try Again</a>"

        # Check if user already exists
        if phone in users:
            return "<h1>❌ User already exists!</h1><a href='/login_page'>Go to Login</a>"

        users[phone] = pw
        save_data(users)
        return redirect(url_for('login_page'))
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    phone = request.form.get('username')
    pw = request.form.get('password')
    user_captcha = request.form.get('captcha_input')
    
    users = load_data()
    
    if users.get(phone) == pw and user_captcha == session.get('captcha'):
        session['user'] = phone
        return redirect(url_for('dashboard'))
    return "<h1>❌ Login Failed!</h1><a href='/login_page'>Try Again</a>"

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user_phone=session['user'])
    return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('welcome'))

if __name__ == '__main__':
    app.run(debug=True)