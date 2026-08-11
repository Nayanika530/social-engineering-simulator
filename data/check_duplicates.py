import pandas as pd

df = pd.read_csv('data/enron_spam_data.csv')
df = df.drop(columns=['Unnamed: 0'])

total_rows = len(df)
unique_messages = df['Message'].nunique()
duplicate_count = total_rows - unique_messages

print(f"Total rows: {total_rows}")
print(f"Unique messages: {unique_messages}")
print(f"Duplicate messages: {duplicate_count}")
print(f"Duplicate percentage: {duplicate_count/total_rows*100:.2f}%")
