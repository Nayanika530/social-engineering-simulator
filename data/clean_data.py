import pandas as pd

df = pd.read_csv('data/enron_spam_data.csv')
df = df.drop(columns=['Unnamed: 0'])

# Drop rows with empty Message
df = df.dropna(subset=['Message'])

# Drop duplicate messages, keep first occurrence
df = df.drop_duplicates(subset=['Message'], keep='first')

print(f"Final row count: {len(df)}")
print(df['Spam/Ham'].value_counts())

# Save cleaned dataset
df.to_csv('data/enron_cleaned.csv', index=False)
print("\nSaved to data/enron_cleaned.csv")
