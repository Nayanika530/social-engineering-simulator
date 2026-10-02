import os
from flask import Flask, render_template, request, jsonify
import joblib
import json
import random
import psutil
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
print("Loading pre-generated email samples...")
with open("data/pregenerated_emails.json", "r", encoding="utf-8") as f:
    samples = json.load(f)
print("Loading classifier model...")
classifier_model = joblib.load("models/classifier_model.pkl")
vectorizer = joblib.load("models/classifier_vectorizer.pkl")
process = psutil.Process(os.getpid())
mem_mb = process.memory_info().rss / 1024 / 1024
print(f"\n>>> ACTUAL MEMORY: {mem_mb:.0f} MB <<<\n")
print("All models loaded. Starting Flask app...")
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/generate_attack", methods=["POST"])
def generate_attack():
    data = request.json or {}
    scenario = data.get("scenario", "").strip()
    target_role = data.get("target_role", "").strip()
    company = data.get("company", "").strip()

    # Filter samples by scenario (case-insensitive)
    matched_samples = [s for s in samples if s.get("scenario", "").lower() == scenario.lower()]
    if matched_samples:
        sample = random.choice(matched_samples)
    else:
        print(f"Warning: No samples found matching scenario '{scenario}'. Falling back to all samples.")
        sample = random.choice(samples)

    generated_email = sample["email"]
    if target_role:
        generated_email = generated_email.replace(sample["role"], target_role)
    if company:
        generated_email = generated_email.replace(sample["company"], company)
    email_vec = vectorizer.transform([generated_email])
    prediction = classifier_model.predict(email_vec)[0]
    confidence = classifier_model.predict_proba(email_vec)[0]
    threat_level = "Phishing" if prediction == 1 else "Safe"
    confidence_score = float(max(confidence)) * 100
    return jsonify({
        "generated_email": generated_email,
        "threat_level": threat_level,
        "confidence": round(confidence_score, 2)
    })

@app.route("/classify_email", methods=["POST"])
def classify_email():
    data = request.json or {}
    email_text = data.get("email_text", "").strip()
    if not email_text:
        return jsonify({"error": "No email text provided"}), 400
    email_vec = vectorizer.transform([email_text])
    prediction = classifier_model.predict(email_vec)[0]
    confidence = classifier_model.predict_proba(email_vec)[0]
    threat_level = "Phishing" if prediction == 1 else "Safe"
    confidence_score = float(max(confidence)) * 100
    return jsonify({
        "threat_level": threat_level,
        "confidence": round(confidence_score, 2)
    })

@app.route("/classify_text", methods=["POST"])
def classify_text():
    return classify_email()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
