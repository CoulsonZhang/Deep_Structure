from bs4 import BeautifulSoup
import re
import requests
import utilities as u
import time
import ujson

with open('names.txt', 'r') as file:
    data = file.read()
    names = data.split('\n')

result = dict()
for i in names:
    time.sleep(2)
    url = u.search(i)
    papers = u.fetch(url)
    result[i] = papers


with open('variable.json', 'w') as file:
    ujson.dump(result, file)

# url = 'https://mathscinet.ams.org/mathscinet/search/publications.html?pg4=AUCN&s4=Gairing%2C+Martin&co4=AND&pg5=TI&s5=&co5=AND&pg6=PC&s6=&co6=AND&pg7=SE&s7=&co7=AND&dr=all&yrop=eq&arg3=&yearRangeFirst=&yearRangeSecond=&pg8=ET&s8=All&review_format=pdf&Submit=Search'
# paper = u.fetch(url)
# for i in paper:
#     print(i)