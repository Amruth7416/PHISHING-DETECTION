from flask import Flask, request, jsonify
from flask_cors import CORS  # Allows frontend to talk to backend

app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route('/detect', methods=['POST'])
def detect_attack():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Invalid request, 'text' field is required"}), 400

    text = data["text"]

    # Simple detection logic (will improve later)
    suspicious_keywords = ["urgent", "password", "click here", "verify"]
    risk_level = "high" if any(word in text.lower() for word in suspicious_keywords) else "low"

    return jsonify({"risk": risk_level, "message": "Possible social engineering attempt!" if risk_level == "high" else "No threat detected."})

if __name__ == '__main__':
    app.run(debug=True)
