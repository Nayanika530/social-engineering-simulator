import pandas as pd

df = pd.read_csv("data/Phishing_Email.csv")
df = df.drop(columns=["Unnamed: 0"])
df = df.dropna(subset=["Email Text"])

total = len(df)
unique = df["Email Text"].nunique()
print(f"Total rows: {total}")
print(f"Unique messages: {unique}")
print(f"Duplicates: {total - unique} ({(total-unique)/total*100:.2f}%)")

print("\nUnique per class:")
print(df.groupby("Email Type")["Email Text"].nunique())
