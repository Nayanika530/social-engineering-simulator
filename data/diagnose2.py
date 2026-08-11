import pandas as pd

df = pd.read_csv('data/enron_spam_data.csv')
df = df.drop(columns=['Unnamed: 0'])
df = df.dropna(subset=['Message'])

df['combo'] = df['Subject'].astype(str) + df['Message'].astype(str)
print("Unique combined (Subject+Message) per class:")
print(df.groupby('Spam/Ham')['combo'].nunique())
