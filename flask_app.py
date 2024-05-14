# flask_app.py
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Endpoint for webhooks
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.is_json:
        data = request.get_json()
        with open('webhook_data.json', 'w') as f:
            json.dump(data, f)  # Save the latest webhook data to a file
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Request must be JSON"}), 400

if __name__ == "__main__":
    app.run(port=5001)  # Run on a separate port to avoid conflicts with Streamlit
