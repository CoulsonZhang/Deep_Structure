# 

import json

with open('data/dict_of_coauthors.json', 'r') as f:
    dict_of_coauthors = json.load(f)

prof = 'Baryshnikov, Yuliy M.' 


coauthors = dict_of_coauthors.get(prof, [])

num_of_coauthors = len(coauthors)

print(f'{prof} has {num_of_coauthors} coauthors.')