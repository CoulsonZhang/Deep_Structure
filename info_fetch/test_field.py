from bs4 import BeautifulSoup
import requests
import utilities as u
import time
import ujson
from itertools import combinations
from itertools import permutations


def find_citation():
    with open('faculties.txt', 'r') as file:
        data = file.read()
        names = data.split('\n')

    result = dict()
    idx = 1
    for i in names:
        print("{}/{}Checking:{}\n".format(idx, len(names), i))
        time.sleep(2)
        url = u.search(i)
        citation = u.fetch_citation(url)
        result[i] = citation
        idx += 1

    with open('citation.json', 'w') as file:
        ujson.dump(result, file)
    return result


def citation_joint():
    with open('citation.json', 'r') as file:
        data = ujson.load(file)

    total_citation = dict()
    for i in data:
        tmp = data[i]
        total_citation[i] = set()
        for k in tmp:
            if tmp[k]:
                for j in tmp[k]:
                    total_citation[i].add(j)

    pairs = combinations(total_citation, 2)
    joint = dict()
    for i in pairs:
        one, two = i
        joint[i] = len(total_citation[one] & total_citation[two])


    with open('citation_joint', 'w') as file:
        ujson.dump(joint, file)


def citation_directed():
    with open('citation.json', 'r') as file:
        data = ujson.load(file)

    total_citation = dict()
    for i in data:
        tmp = data[i]
        total_citation[i] = set()
        for k in tmp:
            if tmp[k]:
                for j in tmp[k]:
                    total_citation[i].add(j)
    pairs = permutations(total_citation, 2) # for (one, two). How many time one takes reference of two's paper
    directed = dict()
    for i in pairs:
        one, two = i
        directed[i] = len(set(data[one]) & total_citation[two])

    with open('citation_directed', 'w') as file:
        ujson.dump(directed, file)

citation_joint()
citation_directed()