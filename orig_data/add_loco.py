import pandas as pd

# df = pd.read_json('prov.json')
df = pd.read_json('oppositional.json')
prov = pd.read_json('oppo.json')
random_row = df.sample(n=1).iloc[0]

#print(random_row['title'])
#print(random_row['txt'])
print(random_row['text'])
print()
#print(random_row['subcorpus'])
print(random_row['category'])
user_input = input("Do you accept this row? (yes/no): ").strip().lower()
while user_input not in ['yes', 'no']:
    user_input = input("Invalid input. Please enter 'yes' or 'no': ").strip().lower()

if user_input == 'yes':
    prov = prov._append(random_row, ignore_index=True)
    prov.to_json('prov.json', orient='records')
    print(f"CONSPIRACY: {len(prov[prov['category'] == 'CONSPIRACY'])}")
    print(f"CRITICAL: {len(prov[prov['subcorpus'] == 'CRITICAL'])}")
else:
    print("Discarded.")
