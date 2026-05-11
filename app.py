from flask import Flask, render_template, request, redirect, url_for, session, flash
import random, smtplib, json, os
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "vip_secret_key_99"

# TERI DETAILS
SENDER_EMAIL = "raoyugalyadav4554@gmail.com" 
APP_PASSWORD = "pkaw axqq nmob dlqm" 
DB_FILE = 'users_db.json'

# User Data Load karne ke liye function
def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

# OTP Bhejne ka function
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
def home():
    return render_template('login.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

# LOGIN PROCESS
@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    users = load_users()
    
    if email in users and users[email] == password:
        return f"<h1>Welcome Back! Aap login ho chuke ho: {email}</h1>"
    else:
        return "<h1>Galat Email ya Password! Pehle Register karein.</h1>"

# SIGNUP REQUEST (Pehle Check karega user hai ya nahi)
@app.route('/signup_request', methods=['POST'])
def signup_request():
    email = request.form.get('email')
    password = request.form.get('password')
    users = load_users()

    # CHECK: Agar user pehle se hai
    if email in users:
        return "<h1>Bhai, ye Email pehle se register hai! Direct Login karo.</h1>"

    otp = str(random.randint(111111, 999999))
    session['temp_user'] = {'email': email, 'password': password, 'otp': otp}
    
    if send_otp(email, otp):
        return render_template('verify.html')
    else:
        return "<h1>Email bhejte waqt error aaya. Settings check karein.</h1>"

# OTP VERIFY & SAVE
@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form.get('otp')
    temp_user = session.get('temp_user')
    
    if temp_user and user_otp == temp_user['otp']:
        users = load_users()
        users[temp_user['email']] = temp_user['password']
        with open(DB_FILE, 'w') as f:
            json.dump(users, f)
        session.pop('temp_user', None)
        return "<h1>Registration Success! Ab aap Login kar sakte hain.</h1>"
    else:
        return "<h1>Galat OTP! Fir se try karein.</h1>"

if __name__ == '__main__':
    app.run(debug=True)
