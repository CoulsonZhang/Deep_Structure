from bs4 import BeautifulSoup
import re
import requests
import utilities as u
import time
from itertools import combinations
import ujson

url = 'https://mathscinet.ams.org//mathscinet/search/publications.html?arg3=&co4=AND&co5=AND&co6=AND&co7=AND&dr=all&pg4=AUCN&pg5=TI&pg6=PC&pg7=SE&pg8=ET&review_format=pdf&s4=Kostochka%2C%20Alexandr%20V.&s5=&s6=&s7=&s8=All&sort=Newest&vfpref=pdf&yearRangeFirst=&yearRangeSecond=&yrop=eq&r=301'
u.fetch(url)


