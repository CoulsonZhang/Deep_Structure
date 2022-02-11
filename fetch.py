from bs4 import BeautifulSoup
import re
import requests

def findnext(start):
    # start = 'https://mathscinet.ams.org//mathscinet/search/publications.html?arg3=&co4=AND&co5=AND&co6=AND&co7=AND&dr=all&pg4=AUCN&pg5=TI&pg6=PC&pg7=SE&pg8=ET&review_format=pdf&s4=Kleinberg%2C%20Jon&s5=&s6=&s7=&s8=All&sort=Newest&vfpref=pdf&yearRangeFirst=&yearRangeSecond=&yrop=eq&r=81'
    data = requests.get(start).content

    content = BeautifulSoup(data, 'html.parser')
    # Matches = content.find('div', {"class": "matches"}).get_text().replace('\n', '')
    # match_num = re.sub(r'\D', "", Matches)

    pages = content.find('div', {"class": "navbar"})

    if len(pages) == 1:  # No next page button
        # print("No next page! gg bro!")
        return False, None
    else:
        currnum = pages.find('span', {"class": "CurrentPage"}).get_text()
        nextnum = pages.findAll('span', {"class": "PageLink"})[-1].get_text()

        if nextnum < currnum:
            # print("End of pages bro, time to stop")
            return False, None
        else:
            next = pages.findAll('span', {"class": "PageLink"})[-1]
            link = 'https://mathscinet.ams.org/' + next.find('a', href=True)['href']
            # print(link)
            return True, link



def fetch(url):
    data = requests.get(url).content

    content = BeautifulSoup(data, 'html.parser')
    Matches = content.find('div', {"class": "matches"}).get_text().replace('\n', '')
    match_num = re.sub(r'\D', "", Matches)
    idx = 0
    papers = dict()

    heads = content.findAll('div', {"class": "headline"})
    for head in heads:
        title = head.find('span', {"class": "title"}).getText()
        ele = head.find('a', {"class": "item_status"}).getText()
        # print(head.getText().replace('\n','').split(ele))
        authors = head.getText().replace('\n', '').split(ele)[1:][0]
        authors = authors.split(title)[:-1][0]
        names = []
        for author in authors.split(';'):
            name = author.strip()
            if name:
                names.append(name)
        papers[title] = names

    next, next_url = findnext(url)
    if next:
        next_paper = fetch(next_url)
        papers.update(next_paper)

    return  papers


url = 'https://mathscinet.ams.org/mathscinet/search/publications.html?pg4=AUCN&s4=Gairing%2C+Martin&co4=AND&pg5=TI&s5=&co5=AND&pg6=PC&s6=&co6=AND&pg7=SE&s7=&co7=AND&dr=all&yrop=eq&arg3=&yearRangeFirst=&yearRangeSecond=&pg8=ET&s8=All&review_format=pdf&Submit=Search'
papers = fetch(url)

with open('tittle,author.txt', 'w') as file:
    for k in papers:
        file.write('Title:\n{}\nAuthor(s):\n{}\n\n'.format(k, papers[k]))

print(len(papers))










