from flask import Flask, render_template, request, session
import random, requests

app = Flask(__name__)
app.secret_key = "courier_final_fix"

# Yahan Courier se mili API KEY daalo
COURIER_AUTH_TOKEN = "PASTE_YOUR_COURIER_API_KEY_HERE"

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

    # Courier API request
    url = "https://api.courier.com/send"
    payload = {
        "message": {
            "to": {"email": email},
            "content": {
                "title": "VIP Verification Code",
                "body": f"Your OTP is: {otp}"
            }
        }
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {COURIER_AUTH_TOKEN}"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 202:
            return render_template('verify.html')
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
