# LLM-Powered Social Engineering Attack Simulator
A two-part AI system that simulates the offense/defense dynamic in phishing attacks: a fine-tuned language model generates realistic social engineering emails, and a separately trained classifier scores their threat level in real time.
**Website live at:** https://social-engineering-simulator-opt1.onrender.com
## How it works
- Generator (System 1): GPT-2 fine-tuned on 5,594 real phishing emails to write scenario-specific social engineering attacks (target role, company, and context configurable by the user).
- Classifier (System 2): TF-IDF + Logistic Regression trained on 17,537 labeled phishing/legitimate emails. Achieves 97.75 percent accuracy on held-out test data.
- Flask app: Connects both systems, generates an attack, classifies it live, and displays the threat assessment with confidence score.

### Message Threat Scanner
- Accepts raw SMS- and WhatsApp-style text messages for real-time phishing and smishing threat assessment via `POST /classify_message`.
- Reuses the existing pre-loaded TF-IDF (5,000 features) + Logistic Regression classifier.
- The classifier was trained on full-length email dataset samples; therefore, short SMS-style text messages may produce less reliable predictions due to lexical and length differences.

### Link Safety Checker
- Analyzes candidate URLs locally using a deterministic, rule-based phishing heuristic engine via `POST /classify_url`.
- Evaluates structural risk indicators including raw IPv4 addresses, URL shortening services, `@` authority symbols, suspicious TLDs (`.xyz`, `.top`, `.zip`, etc.), domain-level brand impersonation, punycode/IDN encoding, unencrypted HTTP usage, and excessive URL length.
- Does NOT use machine learning, does NOT require external APIs or API keys, and never visits, fetches, previews, scrapes, or contacts the supplied URL.
## A deliberate architecture decision
The live deployed version uses a pre-generated batch of Generator outputs, personalized at request time with the user's inputs, rather than running the ~500MB fine-tuned model live, due to free-tier hosting memory constraints (512MB RAM limit). The Classifier still runs 100 percent live for every request. The full Generator model, training pipeline, and fine-tuning notebook are included in this repo for reproducibility.
## Tech stack
- Python, Hugging Face Transformers (fine-tuning)
- scikit-learn (classification)
- Flask (web app)
- Deployed on Render
## Dataset
Phishing Email Detection dataset (18,650 emails, subhajournal on Kaggle), cleaned and deduplicated to 17,537 unique samples before training.
## Running locally
git clone https://github.com/Nayanika530/social-engineering-simulator.git
cd social-engineering-simulator
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/app.py
## Author
Nayanika Halder, B.Tech CSE (Cybersecurity), MAKAUT
