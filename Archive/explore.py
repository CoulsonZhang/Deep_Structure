from bs4 import BeautifulSoup
import re
import requests

url = 'https://mathscinet.ams.org/mathscinet/search/publications.html?pg4=AUCN&s4=+Oren%2C+Sigal+&co4=AND&pg5=TI&s5=&co5=AND&pg6=PC&s6=&co6=AND&pg7=SE&s7=&co7=AND&dr=all&yrop=eq&arg3=&yearRangeFirst=&yearRangeSecond=&pg8=ET&s8=All&review_format=pdf&Submit=Search'

data = requests.get(url).content
content = BeautifulSoup(data, 'html.parser')
heads = content.findAll('div', {"class": "headline"})

for head in heads:
    title = head.find('span', {"class": "title"}).getText()
    # print("Title is:{}".format(title))
    citation = head.find('div', {"class": "headlineMenu"})
    menu_link = []
    for i in citation.findAll('a', href=True):
        menu_link.append(i['href'])

    detail_page = 'https://mathscinet.ams.org/' + menu_link[0]
    citation_page = 'https://mathscinet.ams.org/' + menu_link[-1] if citation.getText().endswith("Citations\n") else None

    print('Title is:{}\ndetail:{}\ncitation:{}\n\n'.format(title, detail_page, citation_page))


    # if citation.getText().endswith("Citations\n"):
    #     # print('x')
    #     # detail_page = 'https://mathscinet.ams.org/' + citation.find('a', href=True)['href']
    #     # citation_page =
    #
    #     for i in citation.findAll('a', href=True):
    #         print('XXX')
    #         print('https://mathscinet.ams.org/' + i['href'])
    #
    # print("HHHH")
    # cites = head.findAll('a', {"target": "NEW"}).getText()
    # for cite in cite:
    #     tex = cite.getTexs()
    #     print(tex)
    # print()


# next = pages.findAll('span', {"class": "PageLink"})[-1]
# link = 'https://mathscinet.ams.org/' + next.find('a', href=True)['href']

# def fetch(url):
#     data = requests.get(url).content
#
#     content = BeautifulSoup(data, 'html.parser')
#     # Matches = content.find('div', {"class": "matches"}).get_text().replace('\n', '')
#     # match_num = re.sub(r'\D', "", Matches)
#     # idx = 0
#     papers = dict()
#
#     heads = content.findAll('div', {"class": "headline"})
#     for head in heads:
#         title = head.find('span', {"class": "title"}).getText()
#         ele = head.find('a', {"class": "item_status"}).getText()
#         # print(head.getText().replace('\n','').split(ele))
#         authors = head.getText().replace('\n', '').split(ele)[1:][0]
#         authors = authors.split(title)[:-1][0]
#         names = []
#         for author in authors.split(';'):
#             name = author.strip()
#             if name:
#                 names.append(name)
#         papers[title] = names