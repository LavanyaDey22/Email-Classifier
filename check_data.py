import pandas as pd
import os
from utils import mask_pii

file_path = 'data/combined_emails_with_natural_pii.csv'

print("✅ Script started")

if os.path.exists(file_path):
    print("✅ Found the CSV file!")

    df = pd.read_csv(file_path)

    print("\n🔹 First 5 rows of data:")
    print(df.head())

    print("\n🔹 Column names:")
    print(df.columns)
else:
    print("❌ File not found at path:", file_path)

from utils import mask_pii

sample_email = """
Hi, my name is Rohan Sharma. My email is rohan.sharma@gmail.com,
and my card number is 1234-5678-9101-1121. My phone is +91 9876543210.
"""

masked, entity_list = mask_pii(sample_email)

print("🔹 Masked Email:")
print(masked)

print("\n🔹 Detected Entities:")
for ent in entity_list:
    print(ent)

masked_emails = []
entity_lists = []

for email in df['email']:
    masked_text, entity_list = mask_pii(email)
    masked_emails.append(masked_text)
    entity_lists.append(entity_list)

df['masked_email'] = masked_emails
df['pii_entities'] = entity_lists

print("\n🔹 Masked dataset preview:")
print(df[['email', 'masked_email', 'type']].head())

X = df['masked_email']           
y = df['type']                   

df.to_csv('data/processed_emails.csv', index=False)
print("\n✅ Saved processed dataset to data/processed_emails.csv")
