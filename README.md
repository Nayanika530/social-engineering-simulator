# LLM-Powered Social Engineering Attack Simulator
A two-part AI system that simulates the offense/defense dynamic in phishing attacks: a fine-tuned language model generates realistic social engineering emails, and a separately trained classifier scores their threat level in real time.
**Live demo:** https://social-engineering-simulator-opt1.onrender.com
## How it works
- Generator (System 1): GPT-2 fine-tuned on 5,594 real phishing emails to write scenario-specific social engineering attacks (target role, company, and context configurable by the user).
- Classifier (System 2): TF-IDF + Logistic Regression trained on 17,537 labeled phishing/legitimate emails. Achieves 97.75 percent accuracy on held-out test data.
- Flask app: Connects both systems, generates an attack, classifies it live, and displays the threat assessment with confidence score.
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
