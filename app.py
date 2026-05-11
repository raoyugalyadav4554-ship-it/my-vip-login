from flask import Flask, render_template, request, session, redirect, url_for
import random, smtplib, json, os
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "final_fix_secure_key_123"

SENDER_EMAIL = "raoyugalyadav4554@gmail.com"
APP_PASSWORD = "auge vxda kndz xlik"

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
    
    otp = str(random.randint(111111, 999999))
    session['temp_user'] = {'email': email, 'password': password, 'otp': otp}
    
    msg = EmailMessage()
    msg.set_content(f"Your VIP Verification Code is: {otp}")
    msg['Subject'] = 'Security Code'
    msg['From'] = SENDER_EMAIL
    msg['To'] = email
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        # Ye line verify.html par le jayegi
        return render_template('verify.html')
    except Exception as e:
        return f"Mail Error: {str(e)}"

@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form.get('otp')
    temp_user = session.get('temp_user')
    if temp_user and user_otp == temp_user['otp']:
        return "<h1>Registration Successful!</h1>"
    return "<h1>Invalid OTP. Try again.</h1>"

if __name__ == '__main__':
    app.run(debug=True)
