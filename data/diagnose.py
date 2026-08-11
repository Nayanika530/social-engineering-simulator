import pandas as pd

df = pd.read_csv('data/enron_spam_data.csv')
df = df.drop(columns=['Unnamed: 0'])
df = df.dropna(subset=['Message'])

print("Before dedup:")
print(df['Spam/Ham'].value_counts())

print("\nUnique messages per class:")
print(df.groupby('Spam/Ham')['Message'].nunique())
