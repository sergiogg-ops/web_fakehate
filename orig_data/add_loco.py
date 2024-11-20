import pandas as pd
import random

df = pd.read_json('LOCO.json')
loco = pd.read_json('loco.json')
random_row = df[df['subcorpus'] == 'conspiracy'].sample(n=1).iloc[0]

print(random_row['title'])
print(random_row['txt'])
print()
print(random_row['subcorpus'])
user_input = input("Do you accept this row? (yes/no): ").strip().lower()
while user_input not in ['yes', 'no']:
    user_input = input("Invalid input. Please enter 'yes' or 'no': ").strip().lower()

if user_input == 'yes':
    loco = loco._append(random_row, ignore_index=True)
    loco.to_json('loco.json', orient='records')
    print(f"Mainstream: {len(loco[loco['subcorpus'] == 'mainstream'])}")
    print(f"Conspiracy: {len(loco[loco['subcorpus'] == 'conspiracy'])}")
else:
    print("Discarded.")
