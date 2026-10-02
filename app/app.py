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
# Mapping from user scenarios to pre-generated attack library categories
SCENARIO_MAPPING = {
    # Password Reset
    "password reset": "password reset",
    "password": "password reset",
    "reset password": "password reset",
    "pwd reset": "password reset",

    # Wire Transfer
    "wire transfer": "urgent wire transfer",
    "urgent wire transfer": "urgent wire transfer",
    "wire": "urgent wire transfer",
    "transfer": "urgent wire transfer",

    # Cloud SSO / Account Verification
    "cloud sso": "account verification",
    "sso": "account verification",
    "cloud": "account verification",
    "account verification": "account verification",
    "account": "account verification",
    "sso login": "account verification",

    # HR Benefits / Software License Renewal
    "hr benefits": "software license renewal",
    "hr": "software license renewal",
    "benefits": "software license renewal",
    "software license renewal": "software license renewal",
    "software license": "software license renewal",
    "license renewal": "software license renewal",
    "license": "software license renewal",

    # Invoice Payment
    "invoice payment": "invoice payment",
    "invoice": "invoice payment",
    "payment": "invoice payment",
}

def resolve_scenario_category(scenario_input: str) -> str:
    """Maps a user-selected scenario to the closest matching category in the pre-generated attack library."""
    if not scenario_input:
        return "password reset"
    norm = scenario_input.strip().lower()
    if norm in SCENARIO_MAPPING:
        return SCENARIO_MAPPING[norm]
    # Check substring matches
    for key, mapped in SCENARIO_MAPPING.items():
        if key in norm or norm in key:
            return mapped
    return norm

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_attack", methods=["POST"])
def generate_attack():
    data = request.json or {}
    scenario = data.get("scenario", "").strip()
    target_role = data.get("target_role", "").strip()
    company = data.get("company", "").strip()

    # 1. Map input scenario to pre-generated library category
    target_category = resolve_scenario_category(scenario)
    matched_samples = [s for s in samples if s.get("scenario", "").lower() == target_category.lower()]

    if matched_samples:
        sample = random.choice(matched_samples)
    else:
        # Fallback if unmapped
        print(f"Warning: No samples found matching scenario '{scenario}' (mapped to '{target_category}'). Falling back to all samples.")
        sample = random.choice(samples)

    # 2. Target Personalization
    generated_email = sample["email"]
    original_role = sample.get("role", "")
    original_company = sample.get("company", "")

    if target_role:
        if original_role and original_role in generated_email:
            generated_email = generated_email.replace(original_role, target_role)
        else:
            for fallback_r in ["Finance Manager", "HR Director", "CEO", "IT Administrator", "Marketing Lead", "Accounts Payable Clerk"]:
                if fallback_r in generated_email:
                    generated_email = generated_email.replace(fallback_r, target_role)
                    break

    if company:
        if original_company and original_company in generated_email:
            generated_email = generated_email.replace(original_company, company)
        else:
            for fallback_c in ["Acme Corp", "Umbrella Corp", "Wayne Enterprises", "Globex Inc", "Initech", "Stark Industries"]:
                if fallback_c in generated_email:
                    generated_email = generated_email.replace(fallback_c, company)
                    break

    # 3. TF-IDF & Logistic Regression Inference
    email_vec = vectorizer.transform([generated_email])
    prediction = classifier_model.predict(email_vec)[0]
    confidence = classifier_model.predict_proba(email_vec)[0]
    threat_level = "Phishing" if prediction == 1 else "Safe"
    confidence_score = float(max(confidence)) * 100

    return jsonify({
        "generated_email": generated_email,
        "threat_level": threat_level,
        "confidence": round(confidence_score, 2),
        "scenario": scenario or sample.get("scenario", "Password Reset"),
        "target_role": target_role or sample.get("role", "Target Role"),
        "company": company or sample.get("company", "Target Organization"),
        "matched_scenario": sample.get("scenario", "")
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
