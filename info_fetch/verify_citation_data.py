import json
import os

path = os.getcwd()

with open(path + '/data/citations/KatzSheldonH_citations.json', 'r') as f:
    data = json.load(f)

name = 'Katz, Sheldon H.'


