import pandas as pd

df = pd.read_csv("data/phishing_cleaned.csv")
phishing_only = df[df["Email Type"] == "Phishing Email"]["Email Text"]

lengths = phishing_only.str.len()

# Keep only emails between 50 and 3000 characters (realistic phishing email range)
filtered = phishing_only[(lengths >= 50) & (lengths <= 3000)]

print(f"Before filtering: {len(phishing_only)}")
print(f"After filtering: {len(filtered)}")
print(f"Removed: {len(phishing_only) - len(filtered)}")

with open("data/generator_training_data.txt", "w", encoding="utf-8") as f:
    for email in filtered:
        f.write(email.strip() + "\n<|endoftext|>\n")

print("\nSaved cleaned version to data/generator_training_data.txt")
