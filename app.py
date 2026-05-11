from flask import Flask, render_template, request, session
import random, smtplib, json, os
from email.message import EmailMessage

app = Flask(__name__, template_folder='templates')
app.secret_key = "force_update_2026"

SENDER_EMAIL = "raoyugalyadav4554@gmail.com" 
APP_PASSWORD = "pkaw axqq nmob dlqm" 
DB_FILE = 'users_db.json'

def load_data():
    if not os.path.exists(DB_FILE): return {}
    with open(DB_FILE, "r") as f: return json.load(f)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/signup_request', methods=['POST'])
def signup_request():
    email = request.form.get('email')
    password = request.form.get('password')
    users = load_data()
    
    if email in users:
        return "<h1>This Email is already registered! Please Login.</h1>"
    
    otp = str(random.randint(111111, 999999))
    session['temp_user'] = {'email': email, 'password': password, 'otp': otp}
    
    # OTP Sending Logic
    msg = EmailMessage()
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = 'VIP Security Code'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        return render_template('verify.html')
    except Exception as e:
        return f"<h1>Mail Error: {str(e)}</h1>"

@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form.get('otp')
    temp_user = session.get('temp_user')
    if temp_user and user_otp == temp_user['otp']:
        users = load_data()
        users[temp_user['email']] = temp_user['password']
        with open(DB_FILE, "w") as f: json.dump(users, f)
        return "<h1>Success! You are now registered. Go to Login page.</h1>"
    return "<h1>Invalid OTP!</h1>"

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    users = load_data()
    if email in users and users[email] == password:
        return f"<h1>Welcome! Logged in as {email}</h1>"
    return "<h1>Login Failed! Invalid email or password.</h1>"

if __name__ == '__main__':
    app.run(debug=True)
