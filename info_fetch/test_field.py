from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import utilities as u
import time
import ujson
from itertools import combinations
from itertools import permutations

with open('data/citations_source.json', 'r') as file:
    data = ujson.load(file)

citePool = set()
citeAuthor = defaultdict(list)
result = defaultdict(int)
for author in data:
    for citation in data[author]:
        if citation:
            citeAuthor[author].append(citation)
            citePool.add(citation)

for author in data:
    for cite in citePool:
        times = citeAuthor[author].count(cite)
        result[(author, cite)] += times

with open('data/cite_pool.json', 'w') as file:
    ujson.dump(result, file)
