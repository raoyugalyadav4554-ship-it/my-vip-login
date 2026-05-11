from flask import Flask, render_template, request, session
import random, smtplib, os
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "victory_key_99"

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
        # TLS use kar rahe hain (Port 587) jo network block nahi hota
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
        server.starttls() 
        server.login("raoyugalyadav4554@gmail.com", "auge vxda kndz xlik")
        server.send_message(msg)
        server.quit()
        return render_template('verify.html')
    except Exception as e:
        return f"<h1>Connection Error: {str(e)}</h1><p>Bhai, Render ka network SMTP block kar raha hai. TLS try kiya hai ab.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
