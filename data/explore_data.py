import pandas as pd

df = pd.read_csv('data/enron_spam_data.csv')
df = df.drop(columns=['Unnamed: 0'])

print("Missing values per column:")
print(df.isnull().sum())

print("\nSpam/Ham distribution:")
print(df['Spam/Ham'].value_counts())

empty_message = df['Message'].isnull().sum()
print(f"\nRows with empty Message: {empty_message}")

print("\nSample spam emails:")
print(df[df['Spam/Ham'] == 'spam'][['Subject', 'Message']].head(3))
