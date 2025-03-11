from flask import Flask, request, jsonify
from flask_cors import CORS 
from models.phrases import predict_phrase  
from models.website import analyze_url 
from models.emails import detect_email  

app = Flask(__name__)
CORS(app)

@app.route('/detect', methods=['POST'])
def detect_attack():
    data = request.get_json()
    
    if not data or "text" not in data:
        return jsonify({"error": "Invalid request, 'text' field is required"}), 400

    text = data["text"]
    
    phrase_result = predict_phrase(text)
    email_result = detect_email(text)
    url_result = analyze_url(text) if "http" in text or "www" in text else "not_a_url"

    risk = "high" if phrase_result == "malicious" or email_result == "suspicious" or url_result == "phishing" else "low"

    return jsonify({
        "risk": risk,
        "phrase_analysis": phrase_result,
        "email_analysis": email_result,
        "url_analysis": url_result if url_result != "not_a_url" else "No URL detected",
        "message": "Possible social engineering attempt!" if risk == "high" else "No threat detected."
    })

if __name__ == '__main__':
    app.run(debug=True)
