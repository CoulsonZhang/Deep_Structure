import json
import os

directory = './data/citations/'


for filename in os.listdir(directory):
    if filename.endswith('.json'):  
        with open(os.path.join(directory, filename), 'r') as f:
            data = json.load(f)

        name = filename.split('_')[0]

        values = list(data.values())
        keys = list(data.keys())

        total_length = 0
        for key in data:
            if isinstance(data[key], list): 
                list_length = len(data[key])
                #print('The number of citations for paper {} is: {}'.format(key, list_length))
                total_length += list_length  

        print('The total number of citations for professor {} is: {}'.format(name, total_length)) 



