from turtle import back
from unicodedata import name
import credential as c
import os
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utilities as u
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import selenium_utilities_funcs as su

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)



#sample input
author_name = 'Ford, Kevin'

# setup
option = webdriver.ChromeOptions()
toolsURL = "https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/index.html"
option.add_argument("headless")
#base_path = os.path.dirname(os.path.abspath(__file__))
#drive_path = os.path.abspath(base_path + "/chromedriver")
#driver = webdriver.Chrome(drive_path)
driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install())
driver.get(toolsURL)
time.sleep(0.2)


# login
driver.find_element_by_xpath("//*[@id='i0116']").click()
time.sleep(0.2)
driver.find_element_by_id("i0116").send_keys(c.username)
time.sleep(0.2)

driver.find_element_by_xpath("//*[@id='idSIButton9']").click()

time.sleep(0.5)

driver.find_element_by_id("i0118").send_keys(c.password)

time.sleep(0.2) # wait 0.2 seconds, waiting for the program to get everything 


driver.find_element_by_xpath("//*[@id='idSIButton9']").click()
time.sleep(2)
#try:
#    element = WebDriverWait(driver, 15).until(
#    EC.presence_of_element_located((By.NAME, "s4"))
#)
#except:
#    driver.quit()
#time.sleep(0.3)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException




def access_author(author_name):
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio'][value='pubyear']"))
        )
        element.click()
    except Exception as e:
        print("Error occurred: ", e)
        
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yrop')))
        select = Select(driver.find_element_by_id('yrop'))
        select.select_by_visible_text('>')
    except Exception as e:
        print("Error while selecting from dropdown: ", e)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yearValue'))).send_keys("2010")
    except Exception as e:
        print("Error while entering year: ", e)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 's4'))).send_keys(author_name)
    except Exception as e:
        print("Error while entering author name: ", e)

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'Submit'))).click()
    except Exception as e:
        print("Error while submitting: ", e)


def check_exists_by_class_name():
    try:
        driver.find_element_by_class_name("reflist")
    except:
        return False
    return True

def back_to_home(author_name):
    driver.find_element_by_link_text("Home").click()
    time.sleep(0.2)
    driver.find_element_by_css_selector("input[type='radio'][value='pubyear']").click()
    time.sleep(0.4)
    select = Select(driver.find_element_by_id('yrop'))
    time.sleep(0.4)
    select.select_by_visible_text('>')
    time.sleep(0.4)
    driver.find_element_by_id("yearValue").send_keys("2010")
    time.sleep(0.4)
    driver.find_element_by_name("s4").send_keys(author_name)
    time.sleep(0.4)
    driver.find_element_by_name("Submit").click()
    time.sleep(0.4)



def get_titles():
    titles = []
    time.sleep(0.2)
    for elem in driver.find_elements_by_xpath('.//span[@class = "title"]'):
        titles.append(elem.text)

    #getting next page
    while (True):
        time.sleep(0.2)
        try: 
            driver.find_element_by_partial_link_text("Next").click()
            time.sleep(0.2)
            for elem in driver.find_elements_by_xpath('.//span[@class = "title"]'):
                titles.append(elem.text)
        except:
            break

    return titles

def get_references(author_name):
    back_to_home(author_name)

    driver.find_element_by_class_name("mrnum").click()

    listreferences = []
    time.sleep(0.2)
    if (check_exists_by_class_name()):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        spans = soup.find_all('a', href = True)
        list_for_paper = []
        for word in spans:
            if (word.get_text()[0:2] == "MR" or word.get_text()[0:2] == "ar"):
                list_for_paper.append(word.get_text())
        listreferences.append(word.get_text())

    else:
        listreferences.append([])

    #keep on adding references until there is no next paper
    while (True):
        time.sleep(0.2)
        try: 
            driver.find_element_by_partial_link_text("Next").click()
            time.sleep(0.2)
            if (check_exists_by_class_name()):
                time.sleep(0.4)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                time.sleep(0.2)
                spans = soup.find_all('a', href = True)
                time.sleep(0.2)
                list_for_paper = []
                for word in spans:
                    if (word.get_text()[0:2] == "MR" or word.get_text()[0:2] == "ar"):
                        list_for_paper.append(word.get_text())
                        
                listreferences.append(list_for_paper)
                time.sleep(0.4)
            else:
                listreferences.append([])
        except:
            break
    return listreferences

def get_journals(author_name):

    back_to_home(author_name)

    driver.find_element_by_class_name("mrnum").click()
    links = []

    soup = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(0.2)
    spans = soup.find_all('a', href = True)
    for link in spans:
        links.append(link['href'])
    journal_ids = []
    for i in range(len(links)):
        if '?id=' in links[i]:
            journal_id = links[i][links[i].index("=") + 1:len(links[i])]
            journal_ids.append(journal_id)
    journal_ids.pop();

    while (True):
        time.sleep(0.2)
        try: 
            driver.find_element_by_partial_link_text("Next").click()
            time.sleep(0.2)
            time.sleep(0.4)
            soup = BeautifulSoup(driver.page_source, "html.parser")
            time.sleep(0.2)
            links = []
            spans = soup.find_all('a', href = True)
            for link in spans:
                links.append(link['href'])
            for i in range(len(links)):
                if '?id=' in links[i]:

                    journal_id = links[i][links[i].index("=") + 1:len(links[i])]
                    journal_ids.append(journal_id)
            journal_ids.pop();
            

        except:
            break
    return journal_ids
           

def get_author_id(author_name):
    back_to_home(author_name)
    driver.find_element_by_class_name("mrnum").click()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(0.2)
    spans = soup.find_all('a', href = True)
    links = []
    for link in spans:
        links.append(link['href'])
    author_id = ""
    for i in range(len(links)):
        if 'authid=' in links[i]:
            author_id = links[i][links[i].index("=") + 1:len(links[i])]
            break

    return author_id
    
def paper_info(name):
    su.search(name)
    print("Done accessing author \n \n")
    author_id = su.get_author_id(name)
    print("Done getting author id\n ")
    titles = get_titles()
    print("Done getting titles\n ")
    references = get_references(name)
    print("Done getting references\n ")
    journals = get_journals(name)
    print("Done getting journals\n ")

    paperdict = {}

    citationdict = su.fetch_citation(su.search(name))
    print(citationdict)


    


    for i in range(len(references)):
        list_of_info = []
        list_of_info.append(author_id)
        list_of_info.append(journals[i])
        list_of_info.append(references[i])

        list_of_info.append(citationdict.get(titles[i]))
        

        paperdict[titles[i]] = list_of_info
        

    
    return (paperdict)


# references = get_references(author_name)
# print(references)
# print(get_titles)
print(paper_info(author_name))

# print(paper_info(author_name))
# # driver.quit()


    
prof_list = ["Ford, Kevin B.",
"Tyson, Jeremy T.",
"Hirani, Anil N.",
"Katz, Sheldon H.",
"Albin, Pierre",
"Dunfield, Nathan M.",
"Kostochka, Alexandr V.",
"Kedem, Rinat",
"Song, Renming",
"Dodd, Christopher",
"Duursma, Iwan Maynard",
"McCarthy, Randy",
"Rezk, Charles W.",
"Fernandes, Rui Loja",
"Mineyev, Igor",
"Dutta, Sankar Prasad",
"Yong, Alexander T. F.",
"Tolman, Susan",
"Erdoğan, Mehmet Burak",
"Junge, Marius",
"Hur, Vera Mikyoung",
"Stojanoska, Vesna",
"Ahlgren, Scott D.",
"Bradlow, Steven Benjamin",
"Rapti, Zoi",
"Sowers, Richard B.",
"Balogh, József",
"Kutzarova, Denka N.",
"Zaharescu, Alexandru",
"La Nave, Gabriele",
"Ando, Matthew",
"Berwick-Evans, Daniel",
"DeVille, R. E. Lee",
"Boca, Florin-Petre",
"Thorner, Jesse",
"Zharnitsky, Vadim",
"Lerman, Eugene M.",
"Reznick, Bruce",
"Dey, Partha Sarathi",
"Hinkkanen, Aimo",
"Nikolaev, Igor G.",
"Pascaleff, James Thomas",
"Bronski, Jared C.",
"Feng, Runhuan",
"Haboush, William J.",
"Baryshnikov, Yuliy M.",
"Kirr, Eduard",
"Oikhberg, Timur",
"Leditzky, Felix",
"Kirkpatrick, Kay Lene",
"Jing, Xiaochen",
"Tzirakis, Nikolaos",
"Kerman, Ely",
"Di Francesco, Philippe",
"Laugesen, Richard Snyder",
"Heller, Jeremiah Ben",
"Guzman, Rosemary K."
"Jing, Xiaochen"
"Liu, Yuan"
"Quan, Zhiyu"
"Fadina,Tolulope"
"Rasmussen, Jacob" 
"Rasmussen, Sarah Dean"
"Janda, Felix"
"Cooney, Daniel B"
"Hung, Pei-Kun"
"Young, Amanda"
"Wu, Xuan"]

for prof in prof_list:
    print(prof)
    print("\n ")
    print(paper_info(prof))
    print("\n ")