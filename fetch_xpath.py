import requests
from lxml import etree


url = 'https://mathscinet.ams.org/mathscinet/search/publications.html?arg3=2010&co4=AND&co5=AND&co6=AND&co7=AND&dr=pubyear&extend=1&pg4=AUCN&pg5=TI&pg6=PC&pg7=SE&pg8=ET&review_format=pdf&s4=&s5=&s6=13&s7=&s8=All&sort=Newest&vfpref=pdf&yearRangeFirst=&yearRangeSecond=&yrop=gt&r=1'
data = requests.get(url)
html_xpath = etree.HTML(data.text)
content = html_xpath.xpath(r'//*[@id="content"]/form/div[3]/div[2]/div/div/div[2]/div[2]/text()[1]')

print(content[0])


