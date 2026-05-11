from flask import Flask, render_template, request, session
import random, smtplib, os
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "secret_key_123"

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
    msg.set_content(f"Your OTP is: {otp}")
    msg['Subject'] = 'Verification Code'
    msg['From'] = "raoyugalyadav4554@gmail.com"
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("raoyugalyadav4554@gmail.com", "auge vxda kndz xlik")
            smtp.send_message(msg)
        return render_template('verify.html')
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
