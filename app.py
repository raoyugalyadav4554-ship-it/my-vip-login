from flask import Flask, render_template, request, session
import random, smtplib, os
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "final_ultra_secure_key"

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/signup_request', methods=['POST'])
def signup_request():
    email = request.form.get('email')
    otp = str(random.randint(111111, 999999))
    session['otp'] = otp

    msg = EmailMessage()
    msg.set_content(f"Your VIP Code: {otp}")
    msg['Subject'] = 'Verification'
    msg['From'] = "raoyugalyadav4554@gmail.com"
    msg['To'] = email

    try:
        # Timeout add kiya hai taaki server ghumta na rahe
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10) as smtp:
            smtp.login("raoyugalyadav4554@gmail.com", "auge vxda kndz xlik")
            smtp.send_message(msg)
        return render_template('verify.html')
    except Exception as e:
        return f"<h1>Mail Error: {str(e)}</h1><p>Check if your App Password is correct.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
