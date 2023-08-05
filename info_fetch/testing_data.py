import json
import os

path = os.getcwd()

with open(path + '/data/author_ids.json', 'r') as f:
    data = json.load(f)


values = list(data.values())
print(values)

keys = list(data.keys())
print(keys)
