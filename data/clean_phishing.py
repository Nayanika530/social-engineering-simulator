import pandas as pd

df = pd.read_csv("data/Phishing_Email.csv")
df = df.drop(columns=["Unnamed: 0"])
df = df.dropna(subset=["Email Text"])
df = df.drop_duplicates(subset=["Email Text"], keep="first")

print(f"Final row count: {len(df)}")
print(df["Email Type"].value_counts())

df.to_csv("data/phishing_cleaned.csv", index=False)
print("\nSaved to data/phishing_cleaned.csv")
