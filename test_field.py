from bs4 import BeautifulSoup
import re
import requests
import utilities as u
import time
from itertools import combinations
import ujson

#This function find the url of "next" button
def findnext(start):
    # start = 'https://mathscinet.ams.org//mathscinet/search/publications.html?arg3=&co4=AND&co5=AND&co6=AND&co7=AND&dr=all&pg4=AUCN&pg5=TI&pg6=PC&pg7=SE&pg8=ET&review_format=pdf&s4=Kleinberg%2C%20Jon&s5=&s6=&s7=&s8=All&sort=Newest&vfpref=pdf&yearRangeFirst=&yearRangeSecond=&yrop=eq&r=81'
    data = requests.get(start).content

    content = BeautifulSoup(data, 'html.parser')
    # Matches = content.find('div', {"class": "matches"}).get_text().replace('\n', '')
    # match_num = re.sub(r'\D', "", Matches)

    pages = content.find('div', {"class": "navbar"})

    if not pages or len(pages) == 1:  # No next page button
        # print("No next page! gg bro!")
        return False, None
    else:
        currnum = pages.find('span', {"class": "CurrentPage"}).get_text()
        nextnum = pages.findAll('span', {"class": "PageLink"})[-1].get_text()

        # print('curr page is: {}\n curr url is:\n{}\n\n'.format(currnum, start))

        if nextnum < currnum:
            # print("End of pages bro, time to stop")
            return False, None
        else:
            next = pages.findAll('span', {"class": "PageLink"})[-1]
            link = 'https://mathscinet.ams.org/' + next.find('a', href=True)['href']
            # print(link)
            return True, link



def fetch_citation(url):
    data = requests.get(url).content

    content = BeautifulSoup(data, 'html.parser')
    # #Key: title Value: citation page url
    # citation = dict() #dict for storing the paper citatoin page (for citation)

    heads = content.findAll('div', {"class": "headline"})
    for head in heads:
        # fetch the title in this paper
        title = head.find('span', {"class": "title"}).getText()
        # fetch the url for detail page & citation page
        citation = head.find('div', {"class": "headlineMenu"})
        menu_link = []
        for i in citation.findAll('a', href=True):
            menu_link.append(i['href'])

        citation_page = 'https://mathscinet.ams.org/' + menu_link[-1] if citation.getText().endswith("Citations\n") else None
        citation[title] = citation_page

    # continue for future work
    next, next_url = findnext(url)
    if next:
        next_paper = fetch_citation(next_url)
        total = {**citation, **next_paper}
        return total
    else:
        return citation

