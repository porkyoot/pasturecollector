# %% [markdown]
# # A Cobblemon Pasture Loot Generator
# 
# This script is meant to create loot tables in `.json` for Minecraft from `.csv` raw data.
# 
# We first install the libraries using `pip`

# %%
#%pip install --upgrade pip

# %% [markdown]
# We then import the libraries in order to use them in the code.

# %%
import csv
import json
import os
import re
from difflib import get_close_matches

# %% [markdown]
# We define the relative paths of the folders. The csv files needs to be in the same folder as the script for convinience

# %%
# Define file paths
drops_csv_path = 'drops.csv'
rolls_csv_path = 'rolls.csv'
output_dir = '../data/pasturecollector/loot_tables/gameplay/pasture_collector/species/'

# %% [markdown]
# We read the rarity chances from the rolls file

# %%

# Read rolls.csv to get the chances
rarity_chances = {}
with open(rolls_csv_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        rarity_chances[row['rarity']] = float(row['chance'].strip('%')) / 100

# %% [markdown]
# We read the csv for items and load them as dictionaries.

# %%
# Define file paths for items CSVs
cobblemon_items_csv_path = 'cobblemon_items.csv'
minecraft_items_csv_path = 'minecraft_items.csv'

# Load items from CSVs into a common dictionary
items_dict = {}

# Load Cobblemon items
with open(cobblemon_items_csv_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        items_dict[row['Item name'].lower()] = row['ID']

# Load Minecraft items
with open(minecraft_items_csv_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        items_dict[row['Item name'].lower()] = row['ID']

print("Items dictionary loaded successfully.")
print(items_dict)

# %%
# Define file path for blacklist CSV
blacklist_csv_path = 'blacklist.csv'

# Read blacklist.csv to get the blacklisted item IDs
blacklisted_items = set()
# Check if BLACKLIST environment variable is set to 'true'
if os.getenv('BLACKLIST', 'false').lower() == 'true':
    with open(blacklist_csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            blacklisted_items.add(row['Item ID'].lower())
    print("Blacklisted items loaded successfully.")
    print(blacklisted_items)
else:
    print("Blacklist is disabled.")

# %% [markdown]
# That's the big one ! We read the drops and for each line we make a json file. For each pokemon the rarity will dictate the random tick chance. For each drop we try to check if it's a valid id, if not we try to match the name perfectly to one in the item list. If all fails we try a near match and give a warning. If it's too far off we throw an error.

# %%
# Read drops.csv and generate JSON files
with open(drops_csv_path, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        pokemon = row['Pokemon'].lower()
        rarity = row['Rarity']
        chance = rarity_chances.get(rarity, 0.0)
        print(f"Processing {pokemon} with rarity {rarity} and chance {chance} ...")
        entries = []
        for i in range(1, 6):
            drop = row[f'Drops{i}']
            #print(f"Drop {i}: {drop}")
            if drop:
                match = re.match(r'([\w\s:]*?)(?:\s([\d\-\.%]+))+$', drop)
                if match:
                    item = match.group(1).lower()
                    count = match.group(2)
                else:
                    item = drop.lower()
                    count = '1'
                
                if item in items_dict.values():
                    item_id = item
                else:
                    item_id = items_dict.get(item)
                if not item_id:
                    close_matches = get_close_matches(item, items_dict.keys(), n=1, cutoff=0.6)
                    if close_matches:
                        item_id = items_dict[close_matches[0]]
                        print(f"Warning: Item '{item}' not found. Using closest match '{close_matches[0]}' instead.")
                    else:
                        print(f"Error: Item '{item}' not found and no close match available.")
                        continue
                if item_id in blacklisted_items:
                    print(f"Warning: Item '{item}' is blacklisted. Skipping.")
                    continue
                if '-' in count:
                    min_count, max_count = map(int, count.split('-'))
                    count = {"min": min_count, "max": max_count}
                elif '%' in count:
                    count = float(count.strip('%')) / 100
                else:
                    count = int(count)
                entries.append({
                    "type": "minecraft:item",
                    "name": item,
                    "functions": [{"function": "minecraft:set_count", "count": count}]
                })
        
        loot_table = {
            "pools": [{
                "rolls": 1,
                "entries": entries,
                "conditions": [{"condition": "minecraft:random_chance", "chance": chance}]
            }]
        }
        
        # Write JSON file
        output_path = os.path.join(output_dir, f'{pokemon}.json')
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Write JSON file
        with open(output_path, mode='w') as json_file:
            json.dump(loot_table, json_file, indent=2)

print("JSON files generated successfully.")


