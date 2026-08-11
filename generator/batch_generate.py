from transformers import pipeline
import json
import random
print("Loading original generator model...")
generator = pipeline("text-generation", model="models/generator/final", tokenizer="models/generator/final")
roles = ["Finance Manager", "HR Director", "IT Administrator", "CEO", "Accounts Payable Clerk", "Marketing Lead"]
companies = ["Acme Corp", "Globex Inc", "Initech", "Umbrella Corp", "Stark Industries", "Wayne Enterprises"]
scenarios = ["password reset", "invoice payment", "urgent wire transfer", "software license renewal", "account verification"]
samples = []
count = 60
print(f"Generating {count} sample phishing emails...")
for i in range(count):
    role = random.choice(roles)
    company = random.choice(companies)
    scenario = random.choice(scenarios)
    prompt = f"Dear {role} at {company}, "
    output = generator(
        prompt,
        max_new_tokens=120,
        num_return_sequences=1,
        temperature=0.8,
        repetition_penalty=1.3,
        no_repeat_ngram_size=3,
        do_sample=True
    )
    generated_text = output[0]["generated_text"]
    samples.append({
        "role": role,
        "company": company,
        "scenario": scenario,
        "email": generated_text
    })
    print(f"  Generated {i+1}/{count}")
with open("data/pregenerated_emails.json", "w", encoding="utf-8") as f:
    json.dump(samples, f, indent=2)
print(f"\nSaved {count} pre-generated emails to data/pregenerated_emails.json")
