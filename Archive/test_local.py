from bs4 import BeautifulSoup
import re

with open('test.html') as file:
    data = file.read()

content = BeautifulSoup(data, 'html.parser')
Matches = content.find('div', {"class": "matches"}).get_text().replace('\n','')
match_num = re.sub(r'\D', "", Matches)


tittle = content.findAll('div', {"class": "headlineText"})
for i in tittle:
    print(i.get_text())

# c1 = content.find('div', {"class": "headline"})
# print(c1)