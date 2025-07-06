from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Replace with your actual Twilio Account SID and Auth Token
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")  # Your Twilio phone number (e.g., "+1XXXXXXXXXX")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/send-checkin', methods=['POST'])
def send_checkin():
    data = request.get_json()
    to_number = data.get('to')
    message_body = data.get('message')

    if not to_number or not message_body:
        return jsonify({"error": "Missing 'to' or 'message' parameter"}), 400

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        return jsonify({"status": "Message sent", "sid": message.sid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)