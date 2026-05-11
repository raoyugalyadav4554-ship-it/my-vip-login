from flask import Flask, render_template, request, redirect, url_for, session, flash
import random, smtplib, json, os
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "vip_secret_key_2026"

# SENDER DETAILS
SENDER_EMAIL = "raoyugalyadav4554@gmail.com" 
APP_PASSWORD = "pkaw axqq nmob dlqm" 
DB_FILE = 'users_db.json'

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {}

def send_otp(receiver_email, otp):
    msg = EmailMessage()
    msg.set_content(f"Your VIP Security OTP is: {otp}")
    msg['Subject'] = 'Security Verification Code'
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
    users = load_users()
    if email in users and users[email] == password:
        return f"<h1>Welcome! Logged in as: {email}</h1>"
    return "<h1>Invalid Credentials! Please try again.</h1>"

@app.route('/signup_request', methods=['POST'])
def signup_request():
    email = request.form.get('email')
    password = request.form.
