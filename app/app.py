import os
import ipaddress
import urllib.parse
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

# ==============================================================================
# DEFENSIVE FEATURE 1: MESSAGE / SMS PHISHING DETECTION
# ==============================================================================

@app.route("/classify_message", methods=["POST"])
def classify_message():
    """Classifies SMS/WhatsApp-style messages using the pre-loaded email classifier model.
    Note: The classifier was trained on email data; short SMS text may have different lexical distribution.
    """
    if not request.is_json:
        return jsonify({"error": "message_text is required and must be a non-empty string"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "message_text" not in data:
        return jsonify({"error": "message_text is required and must be a non-empty string"}), 400

    message_text = data.get("message_text")
    if not isinstance(message_text, str) or not message_text.strip():
        return jsonify({"error": "message_text is required and must be a non-empty string"}), 400

    # Reuse pre-loaded TF-IDF vectorizer and Logistic Regression classifier
    message_vec = vectorizer.transform([message_text])
    prediction = classifier_model.predict(message_vec)[0]
    confidence = classifier_model.predict_proba(message_vec)[0]
    threat_level = "Phishing" if prediction == 1 else "Safe"
    confidence_score = float(max(confidence)) * 100

    return jsonify({
        "threat_level": threat_level,
        "confidence": round(confidence_score, 2),
        "note": "Classifier trained on email data; may be less accurate on short SMS-style text."
    })

# ==============================================================================
# DEFENSIVE FEATURE 2: URL / LINK SAFETY CHECKER (RULE-BASED HEURISTICS)
# ==============================================================================

# Brand to authentic primary domain mapping for brand impersonation heuristic
KNOWN_BRANDS = {
    "paypal": "paypal.com",
    "amazon": "amazon.com",
    "google": "google.com",
    "microsoft": "microsoft.com",
    "apple": "apple.com",
    "netflix": "netflix.com",
}

# Known URL shortener services (medium risk flag)
SHORTENER_DOMAINS = {
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "goo.gl",
    "ow.ly",
    "is.gd",
}

# Suspicious or commonly abused TLDs (medium risk flag)
SUSPICIOUS_TLDS = {
    ".xyz",
    ".top",
    ".club",
    ".work",
    ".click",
    ".link",
    ".zip",
}

# Severity-based heuristic score weights:
# HIGH-RISK FLAGS (40 points each):
#   - IP address instead of domain       : 40 points
#   - @ symbol in URL authority          : 40 points
#   - Brand impersonation in hostname    : 40 points
# MEDIUM-RISK FLAGS (20 points each):
#   - URL shortening service             : 20 points
#   - Excessive hyphens in hostname (>=2): 20 points
#   - Suspicious or commonly abused TLD  : 20 points
#   - Punycode / IDN encoding (xn--)     : 20 points
# LOW-RISK FLAGS (10 points each):
#   - No HTTPS (http:// scheme)          : 10 points
#   - Unusually long URL (> 75 chars)    : 10 points
# Maximum score is capped at 100 points.

def analyze_url_heuristics(raw_url: str):
    """Deterministically evaluates a URL using local phishing heuristics.
    Never connects, fetches, scrapes, or performs DNS lookups for the target URL.
    Returns analysis dict or None if the URL is malformed.
    """
    url_stripped = raw_url.strip()
    try:
        parsed = urllib.parse.urlsplit(url_stripped)
    except Exception:
        return None

    scheme = (parsed.scheme or "").lower()
    if scheme not in ("http", "https"):
        return None

    if not parsed.netloc:
        return None

    try:
        hostname = (parsed.hostname or "").lower()
        # Validate port if present (raises ValueError on invalid port)
        _ = parsed.port
    except ValueError:
        return None

    if not hostname:
        return None

    flags_triggered = []
    high_risk_count = 0
    medium_risk_count = 0
    score = 0

    # --------------------------------------------------------------------------
    # 1. HIGH-RISK FLAGS
    # --------------------------------------------------------------------------

    # A. IP address instead of domain (Weight: 40)
    is_ip = False
    try:
        ipaddress.ip_address(hostname)
        is_ip = True
    except ValueError:
        is_ip = False

    if is_ip:
        flags_triggered.append("URL uses an IP address instead of a domain name")
        score += 40
        high_risk_count += 1

    # B. @ symbol in authority (Weight: 40)
    # The @ character before the host can obscure the real destination in RFC 3986 authorities
    if "@" in parsed.netloc:
        flags_triggered.append("URL contains an @ symbol that may obscure the actual destination")
        score += 40
        high_risk_count += 1

    # C. Brand impersonation (Weight: 40)
    # Applied strictly to the hostname/domain only; path contents are excluded.
    # Normalizes common leetspeak substitutions (1->l, 0->o, 5->s, 3->e) to detect typosquatting.
    leet_trans = str.maketrans({"1": "l", "0": "o", "5": "s", "3": "e"})
    norm_hostname = hostname.translate(leet_trans)

    brand_impersonated = False
    for brand, legit_domain in KNOWN_BRANDS.items():
        is_legit = (hostname == legit_domain or hostname.endswith("." + legit_domain))
        if not is_legit:
            if brand in hostname or brand in norm_hostname:
                brand_impersonated = True
                break

    if brand_impersonated:
        flags_triggered.append("Domain appears to impersonate a known brand")
        score += 40
        high_risk_count += 1

    # --------------------------------------------------------------------------
    # 2. MEDIUM-RISK FLAGS
    # --------------------------------------------------------------------------

    # D. URL shortener service (Weight: 20)
    is_shortener = (hostname in SHORTENER_DOMAINS or any(hostname.endswith("." + s) for s in SHORTENER_DOMAINS))
    if is_shortener:
        flags_triggered.append("URL uses a URL-shortening service")
        score += 20
        medium_risk_count += 1

    # E. Excessive hyphens in domain (Weight: 20)
    # Deterministic threshold: 2 or more hyphens in the hostname indicates suspicious domain chaining
    if hostname.count("-") >= 2:
        flags_triggered.append("Domain contains an unusually high number of hyphens")
        score += 20
        medium_risk_count += 1

    # F. Suspicious/rare TLD (Weight: 20)
    if any(hostname.endswith(tld) for tld in SUSPICIOUS_TLDS):
        flags_triggered.append("URL uses a suspicious or commonly abused TLD")
        score += 20
        medium_risk_count += 1

    # G. Punycode / IDN encoding (Weight: 20)
    labels = hostname.split(".")
    if any(label.startswith("xn--") for label in labels):
        flags_triggered.append("Domain uses punycode/IDN encoding and may require additional scrutiny")
        score += 20
        medium_risk_count += 1

    # --------------------------------------------------------------------------
    # 3. LOW-RISK FLAGS
    # --------------------------------------------------------------------------

    # H. No HTTPS (Weight: 10)
    if scheme == "http":
        flags_triggered.append("URL does not use HTTPS")
        score += 10

    # I. Unusually long URL (Weight: 10)
    # Threshold: URL exceeding 75 characters
    if len(url_stripped) > 75:
        flags_triggered.append("URL is unusually long")
        score += 10

    # Cap score at 100
    risk_score = min(score, 100)

    # Risk mapping:
    # - Any high-risk flag present                          -> High Risk
    # - No high-risk flags AND 2 or more medium-risk flags  -> Medium Risk
    # - Otherwise                                           -> Low Risk
    if high_risk_count > 0:
        risk_level = "High Risk"
    elif medium_risk_count >= 2:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "flags_triggered": flags_triggered,
        "url_checked": raw_url
    }

@app.route("/classify_url", methods=["POST"])
def classify_url():
    """Deterministically evaluates a URL against phishing heuristics without contacting the server."""
    if not request.is_json:
        return jsonify({"error": "url is required and must be a non-empty string"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "url" not in data:
        return jsonify({"error": "url is required and must be a non-empty string"}), 400

    raw_url = data.get("url")
    if not isinstance(raw_url, str) or not raw_url.strip():
        return jsonify({"error": "url is required and must be a non-empty string"}), 400

    result = analyze_url_heuristics(raw_url)
    if result is None:
        return jsonify({"error": "url is required and must be a non-empty string"}), 400

    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

