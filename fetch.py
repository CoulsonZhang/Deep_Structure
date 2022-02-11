from bs4 import BeautifulSoup
import re
import requests

url = 'https://mathscinet.ams.org/mathscinet/search/publications.html?arg3=2010&co4=AND&co5=AND&co6=AND&co7=AND&dr=pubyear&extend=1&pg4=AUCN&pg5=TI&pg6=PC&pg7=SE&pg8=ET&review_format=pdf&s4=&s5=&s6=13&s7=&s8=All&sort=Newest&vfpref=pdf&yearRangeFirst=&yearRangeSecond=&yrop=gt&r=1'
data = requests.get(url).content


content = BeautifulSoup(data, 'html.parser')
Matches = content.find('div', {"class": "matches"}).get_text().replace('\n','')
match_num = re.sub(r'\D', "", Matches)

idx = 0

# head = content.find('div', {"class": "headline"})
# title = head.find('span', {"class": "title"}).getText()
# ele = head.find('a', {"class": "item_status"}).getText()
#
#
# authors = head.getText().split(ele+'\n\n')[1:][0]
# authors = authors.split(title)[:-1][0]
# names = []
# for author in authors.split(';'):
#     name = author.strip()
#     if name:
#         names.append(name)
#
# print(names)

papers = dict()

heads = content.findAll('div', {"class": "headline"})
for head in heads:
    title = head.find('span', {"class": "title"}).getText()
    ele = head.find('a', {"class": "item_status"}).getText()
    # print(head.getText().replace('\n','').split(ele))
    authors = head.getText().replace('\n','').split(ele)[1:][0]
    authors = authors.split(title)[:-1][0]
    names = []
    for author in authors.split(';'):
        name = author.strip()
        if name:
            names.append(name)
    papers[title] = names

with open('tittle,author.txt', 'w') as file:
    for k in papers:
        file.write('Title:\n{}\nAuthor(s):\n{}\n\n'.format(k,papers[k]))









