from flask import Flask, render_template, request, redirect, url_for, session
import random, smtplib, json, os
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "vip_permanent_key_2026"

# EMAIL SETTINGS
SENDER_EMAIL = "raoyugalyadav4554@gmail.com" 
APP_PASSWORD = "pkaw axqq nmob dlqm" 
DB_FILE = 'users_db.json'

def load_data():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f: return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f: json.dump(data, f)

def send_otp(receiver_email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your VIP Security OTP is: {otp}")
    msg['Subject'] = 'Verification Code'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        return True
    except: return False

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    users = load_data()
    if email in users and users[email] == password:
        return f"<h1>Welcome! Logged in as: {email}</h1>"
    return "<h1>Invalid Credentials! Please try again.</h1>"

@app.route('/signup_request', methods=['POST'])
def signup_request():
    email = request.form.get('email')
    password = request.form.get('password')
    users = load_data()
    if email in users:
        return "<h1>User already exists! Please Login.</h1>"
    otp = str(random.randint(111111, 999999))
    session['temp_user'] = {'email': email, 'password': password, 'otp': otp}
    if send_otp(email, otp):
        return render_template('verify.html')
    return "<h1>Error sending OTP. Check App Password.</h1>"

@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form.get('otp')
    temp_user = session.get('temp_user')
    if temp_user and user_otp == temp_user['otp']:
        users = load_data()
        users[temp_user['email']] = temp_user['password']
        save_data(users)
        session.pop('temp_user', None)
        return "<h1>Registration Success! Now you can Login.</h1>"
    return "<h1>Invalid OTP!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
