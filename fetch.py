from bs4 import BeautifulSoup
import re
import requests

url = 'https://mathscinet.ams.org/mathscinet/search/publications.html?arg3=2010&co4=AND&co5=AND&co6=AND&co7=AND&dr=pubyear&extend=1&pg4=AUCN&pg5=TI&pg6=PC&pg7=SE&pg8=ET&review_format=pdf&s4=&s5=&s6=13&s7=&s8=All&sort=Newest&vfpref=pdf&yearRangeFirst=&yearRangeSecond=&yrop=gt&r=1'
data = requests.get(url).content


content = BeautifulSoup(data, 'html.parser')
Matches = content.find('div', {"class": "matches"}).get_text().replace('\n','')
match_num = re.sub(r'\D', "", Matches)

idx = 0

papers = dict()

heads = content.findAll('div', {"class": "headline"})
for head in heads:
    title = head.find('span', {"class": "title"}).getText()
    author = head.getText().split(title)[0]
    author = head.getText().split(';')
    print(author)
    author[0] = author[0].split('\n')[-1]
    for i in range(len(author)):
        author[i] = author[i].strip()

    print("Tittle:\n{}\nAuthor:\n{}\n\n".format(title,author))









