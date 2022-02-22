from bs4 import BeautifulSoup
import re
from itertools import combinations
import requests
import time
import ujson

# This function read variable joint
# output the joint
def find_joint():
    with open('variable.json') as file:
        result = ujson.load(file)

    pairs = combinations(result, 2)
    joint = dict()
    for i in pairs:
        one, two = i
        num = 0
        for paper in result[one]:
            if two in result[one][paper]:
                num += 1
        joint[i] = num

    print(joint)
    with open('joint.json', 'w') as file:
        ujson.dump(joint, file)


#This function read author names in certain files and fetch publication informatoins
# for the authors.
# structure: list of authors names [].
# Each element in list is a dict(), with paper title as key, list of authors' name of this paper is value
def fetch_list():
    with open('faculties.txt', 'r') as file:
        data = file.read()
        names = data.split('\n')

    result = dict()
    for i in names:
        time.sleep(2)
        url = search(i)
        papers = fetch(url)
        result[i] = papers

    with open('variable.json', 'w') as file:
        ujson.dump(result, file)
    return result

#This function find the url for searching result of input name
def search(name):
    first = 'https://mathscinet.ams.org/mathscinet/search/publications.html?pg4=AUCN&s4='
    second = '&co4=AND&pg5=TI&s5=&co5=AND&pg6=PC&s6=&co6=AND&pg7=SE&s7=&co7=AND&dr=all&yrop=eq&arg3=&yearRangeFirst=&yearRangeSecond=&pg8=ET&s8=All&review_format=pdf&Submit=Search'
    return first + name + second


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


#This function extracts the info from the input url page
def fetch(url):
    data = requests.get(url).content

    content = BeautifulSoup(data, 'html.parser')
    #Key: title Value: list of author name
    papers = dict() #dict for store the paper info.
    #
    # #Key: title Value: detail page url
    # details = dict() #dict for storing the paper detail page (for reference)
    #
    # #Key: title Value: citation page url
    # citation = dict() #dict for storing the paper citatoin page (for citation)

    heads = content.findAll('div', {"class": "headline"})
    for head in heads:
        # fetch the title in this paper
        title = head.find('span', {"class": "title"}).getText()
        ele = head.find('a', {"class": "item_status"}).getText()
        authors = head.getText().replace('\n', '').split(ele)[1:][0]

        try:
            authors = authors.split(title)[:-1][0]
        except IndexError:
            # print('Wrong: title:{}\nauthor_list:{}\nurl:{}\n'.format(title,authors, url))
            authors = authors.split(title.replace('\n', ''))[:-1][0]
            print(authors)
            # print(extra)
            # print('XXX')
            # print(title)
            # print(authors.split(title))
            # print("XXXXX")
            # print(authors)
            # print(title.replace('\n', "" ) in authors)




        names = []
        for author in authors.split(';'):
            name = author.strip()
            if name:
                names.append(name)
        papers[title] = names
    # continue for future work
    next, next_url = findnext(url)
    if next:
        next_paper = fetch(next_url)
        total = {**papers, **next_paper}
        return total
    else:
        return papers




        # # fetch the url for detail page & citation page
        # citation = head.find('div', {"class": "headlineMenu"})
        # menu_link = []
        # for i in citation.findAll('a', href=True):
        #     menu_link.append(i['href'])
        #
        # detail_page = 'https://mathscinet.ams.org/' + menu_link[0]
        # citation_page = 'https://mathscinet.ams.org/' + menu_link[-1] if citation.getText().endswith("Citations\n") else None
        # details[title] = detail_page
        # citation[title] = citation_page


# #write current info
#     with open('tittle,author.txt', 'a') as file:
#         for k in papers:
#             file.write('Title:\n{}\nAuthor(s):\n{}\n\n'.format(k, papers[k]))
#

#
#
# url = 'https://mathscinet.ams.org/mathscinet/search/publications.html?pg4=AUCN&s4=+Oren%2C+Sigal+&co4=AND&pg5=TI&s5=&co5=AND&pg6=PC&s6=&co6=AND&pg7=SE&s7=&co7=AND&dr=all&yrop=eq&arg3=&yearRangeFirst=&yearRangeSecond=&pg8=ET&s8=All&review_format=pdf&Submit=Search'
# fetch(url)


# papers = fetch(url)

# with open('tittle,author.txt', 'a') as file:
#     for k in papers:
#         file.write('Title:\n{}\nAuthor(s):\n{}\n\n'.format(k, papers[k]))

# print(len(papers))










