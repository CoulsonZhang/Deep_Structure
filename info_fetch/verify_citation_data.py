import json
import os

path = os.getcwd()

with open(path + '/data/citations/KatzSheldonH_citations.json', 'r') as f:
    data = json.load(f)

name = 'Katz, Sheldon H.'

values = list(data.values())
keys = list(data.keys())

total_length = 0
for key in data:
    if isinstance(data[key], list): 
        list_length = len(data[key])
        print('The number of citations for paper {} is: {}'.format(key, list_length))
        total_length += list_length  

print('The total number of citations for professor {} is: {}'.format(name, total_length)) 
