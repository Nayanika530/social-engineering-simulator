from flask import Flask, render_template, request, jsonify
import joblib
import json
import random
import psutil
import os
app = Flask(__name__)
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
    data = request.json
    scenario = data.get("scenario", "")
    target_role = data.get("target_role", "")
    company = data.get("company", "")
    # Pick a random pre-generated sample, then personalize it with the user's actual inputs
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
if __name__ == "__main__":
    app.run(debug=False)
