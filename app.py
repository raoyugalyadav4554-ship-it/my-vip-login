from flask import Flask, render_template, request, redirect, url_for, session, flash
import random, smtplib, json, os
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "vip_secret_key_99"

# TERI DETAILS
SENDER_EMAIL = "raoyugalyadav4554@gmail.com" 
APP_PASSWORD = "pkaw axqq nmob dlqm" 

DB_FILE = 'users_db.json'

def send_otp(receiver_email, otp):
    msg = EmailMessage()
    msg.set_content(f"Aapka VIP System OTP hai: {otp}")
    msg['Subject'] = 'VIP Security OTP'
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        return True
    except: return False

@app.route('/')
def home(): return render_template('login.html')

@app.route('/signup_request', methods=['POST'])
def signup_request():
    email = request.form.get('email'); password = request.form.get('password')
    otp = str(random.randint(111111, 999999))
    session['temp_user'] = {'email': email, 'password': password, 'otp': otp}
    if send_otp(email, otp): return render_template('verify.html')
    return "<h1>Email Error! Check App Password.</h1>"

@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form.get('otp'); temp_user = session.get('temp_user')
    if temp_user and user_otp == temp_user['otp']:
        users = {}
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r') as f: users = json.load(f)
        users[temp_user['email']] = temp_user['password']
        with open(DB_FILE, 'w') as f: json.dump(users, f)
        return "<h1>Success! Account Ban Gaya. Ab Login Karo.</h1>"
    return "<h1>Galat OTP hai Bhai!</h1>"

if __name__ == '__main__': app.run(debug=True)
