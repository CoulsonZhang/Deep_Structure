import os
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import credential as c
from selenium.webdriver.common.keys import Keys
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.expected_conditions import url_to_be
import re
import time
start_time = time.time()

# list_of_profs = ["Ford, Kevin B.",
# "Tyson, Jeremy T.",
# "Hirani, Anil N.",
# "Katz, Sheldon H.",
# "Albin, Pierre",
# "Dunfield, Nathan M.",
# "Kostochka, Alexandr V.",
# "Kedem, Rinat",
# "Song, Renming",
# "Dodd, Christopher",
# "Duursma, Iwan Maynard",
# "McCarthy, Randy",
# "Rezk, Charles W.",
# "Fernandes, Rui Loja",
# "Mineyev, Igor",
# "Dutta, Sankar Prasad",
# "Yong, Alexander T. F.",
# "Tolman, Susan",
# "Erdoğan, Mehmet Burak",
# "Junge, Marius",
# "Hur, Vera Mikyoung",
# "Stojanoska, Vesna",
# "Ahlgren, Scott D.",
# "Bradlow, Steven Benjamin",
# "Rapti, Zoi",
# "Sowers, Richard B.",
# "Balogh, József",
# "Kutzarova, Denka N.",
# "Zaharescu, Alexandru",
# "La Nave, Gabriele",
# "Berwick-Evans, Daniel",
# "DeVille, R. E. Lee",
# "Boca, Florin-Petre",
# "Thorner, Jesse",
# "Zharnitsky, Vadim",
# "Lerman, Eugene M.",
# "Reznick, Bruce",
# "Dey, Partha Sarathi",
# "Hinkkanen, Aimo",
# "Nikolaev, Igor G.",
# "Pascaleff, James Thomas",
# "Bronski, Jared C.",
# "Feng, Runhuan",
# "Haboush, William J.",
# "Baryshnikov, Yuliy M.",
# "Kirr, Eduard",
# "Oikhberg, Timur",
# "Leditzky, Felix",
# "Kirkpatrick, Kay Lene",
# "Tzirakis, Nikolaos",
# "Kerman, Ely",
# "Di Francesco, Philippe",
# "Laugesen, Richard Snyder",
# "Heller, Jeremiah Ben",
# "Guzman, Rosemary K.",
# "Jing, Xiaochen",
# "Liu, Yuan",
# "Quan, Zhiyu",
# "Fadina, Tolulope",
# "Rasmussen, Jacob",
# "Rasmussen, Sarah Dean",
# "Janda, Felix",
# "Cooney, Daniel B",
# "Hung, Pei-Ken",
# "Young, Amanda",
# "Wu, Xuan"]

list_of_profs = ["Wei, Wei"]

path = os.getcwd()

with open(path + '/data/author_ids.json', 'r') as f:
    author_ids = json.load(f)

# list_of_profs = list(author_ids.keys())

# setup
option = webdriver.ChromeOptions()
toolsURL = "https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet"
option.add_argument("headless")
#base_path = os.path.dirname(os.path.abspath(__file__))
#drive_path = os.path.abspath(base_path + "/chromedriver")
#driver = webdriver.Chrome(drive_path)
driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install())
driver.get(toolsURL)
time.sleep(1)


# login
driver.find_element_by_xpath("//*[@id='i0116']").click()
time.sleep(0.5)
driver.find_element_by_id("i0116").send_keys(c.username)
time.sleep(0.2)

driver.find_element_by_xpath("//*[@id='idSIButton9']").click()

time.sleep(0.5)

driver.find_element_by_id("i0118").send_keys(c.password)

time.sleep(0.2) # wait 0.2 seconds, waiting for the program to get everything 


driver.find_element_by_xpath("//*[@id='idSIButton9']").click()
time.sleep(15)
#try:
#    element = WebDriverWait(driver, 15).until(
#    EC.presence_of_element_located((By.NAME, "s4"))
#)
#except:
#    driver.quit()
#time.sleep(0.3)

time_elapsed = time.time() - start_time
print(f'Time elapsed so far: {time_elapsed} seconds')

#check if there is next paper


def check_exists_by_partial_link_text():
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Next")))
        return True
    except:
        return False


#check if there is reference list for each author
def check_refs_exist():
    try:
        WebDriverWait(driver, 2.5).until(EC.presence_of_element_located((By.CLASS_NAME, "reflist")))
        return True
    except:
        return False


data = {}




for prof in list_of_profs:
    print("Now searching for " + prof + "'s references, " + str(list_of_profs.index(prof)) + "/" + str(len(list_of_profs)) + " profs")
    time.sleep(0.4)


    if prof in author_ids.keys():
        author_id = author_ids[prof]
        print("Found author_id", author_id)

    data[prof] = {"AuthorID": author_id, "Papers": {}}

    pubs_url = f"https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/search/publications.html?pg1=INDI&s1={author_id}"

    time.sleep(1)
    
    WebDriverWait(driver, timeout=30).until(url_to_be(toolsURL))

    if driver.current_url == toolsURL:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
    driver.get(pubs_url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'mrnum')))
        driver.find_element_by_class_name("mrnum").click()
    except Exception as e:
        print("Error while clicking on mrnum: ", e)


    paper_number = 1
    listreferences = []
    listofpapertitles = []
    listofjournals = []

    time.sleep(0.2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    headline = soup.find('div', {'class': 'headline'})
    # print(headline.prettify())

    # Extract the paper title
    paper_title_element = headline.find('span', {'class': 'title'})
    paper_title = paper_title_element.text if paper_title_element else None

    # Extract the paper ID
    paper_id_element = headline.find('a', attrs={'name': re.compile('^MR')})
    paper_id = paper_id_element['name'] if paper_id_element else None

    # Extract author names and mrauthid
    author_elements = headline.find_all('a', href=re.compile('/mathscinet/2006/mathscinet/search/author.html'))
    authors = [(author_el.text, author_el['href'].split('=')[-1]) for author_el in author_elements]

    # Extract the journal name and ID
    journal_element = headline.find('a', href=re.compile('/mathscinet/2006/mathscinet/search/journaldoc'))
    journal_name = journal_element.em.text if journal_element and journal_element.em else None
    journal_id = journal_element['href'].split('=')[-1] if journal_element else None

    # Extract the publication year
    year_element = headline.find('span', class_='date')
    pub_year = None
    if year_element and year_element.text.isdigit():
        pub_year = year_element.text

    # find the a tag that has classification codes
    all_a_tags = headline.find_all('a')
    for a_tag in all_a_tags:
        href = a_tag.get('href')
        if href and "/mathscinet/2006/mathscinet/search/mscdoc.html?code=" in href:
            code_element = a_tag
            break
    if code_element:
        codes_url = code_element['href']
        codes = codes_url.split('=')[-1]
    else:
        codes = None



    # Print all collected information for verification
    print(f'Paper title: {paper_title}')
    print(f'Paper ID: {paper_id}')
    print(f'Authors: {authors}')
    print(f'Journal Name and ID: {(journal_name, journal_id)}')
    print(f'Publication Year: {pub_year}')
    print('Codes:', codes)


    if (check_refs_exist()):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        spans = soup.find_all('a', href = True)
        print("Getting references for first paper")
        for word in spans:
            if (word.get_text()[0:2] == "MR" or word.get_text()[0:2] == "ar"):
                listreferences.append(word.get_text())
    #print("Done getting references for first paper \n", listreferences)

    data[prof]["Papers"][paper_id] = {
        "Title": paper_title,
        "PaperID": paper_id, 
        "Authors": authors,
        "Journal_Name": journal_name,
        "Publication_Year": pub_year,
        "References": listreferences,
        "Codes": codes
    }

    while (True):
        time.sleep(0.2)
        try: 
            paper_number += 1

            listreferences = []

            time_elapsed = time.time() - start_time
            print(f"Time elapsed: {time_elapsed / 60} minutes. Retrieving data for paper number {paper_number} of {prof}...")
            driver.find_element_by_partial_link_text("Next").click()
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            headline = soup.find('div', {'class': 'headline'})
            time.sleep(1)

            # Extract the paper title
            paper_title_element = headline.find('span', {'class': 'title'})
            paper_title = paper_title_element.text if paper_title_element else None

            # Extract the paper ID
            paper_id_element = headline.find('a', attrs={'name': re.compile('^MR')})
            paper_id = paper_id_element['name'] if paper_id_element else None

            # Extract author names and mrauthid
            author_elements = headline.find_all('a', href=re.compile('/mathscinet/2006/mathscinet/search/author.html'))
            authors = [(author_el.text, author_el['href'].split('=')[-1]) for author_el in author_elements]

            # Extract the journal name and ID
            journal_element = headline.find('a', href=re.compile('/mathscinet/2006/mathscinet/search/journaldoc'))
            journal_name = journal_element.em.text if journal_element and journal_element.em else None
            journal_id = journal_element['href'].split('=')[-1] if journal_element else None

            # Extract the publication year
            year_element = headline.find('span', class_='date')
            pub_year = None
            if year_element and year_element.text.isdigit():
                pub_year = year_element.text

            # find the a tag
            all_a_tags = headline.find_all('a')
            for a_tag in all_a_tags:
                href = a_tag.get('href')
                if href and "/mathscinet/2006/mathscinet/search/mscdoc.html?code=" in href:
                    code_element = a_tag
                    break
            if code_element:
                codes_url = code_element['href']
                codes = codes_url.split('=')[-1]
            else:
                codes = None



            # Print all collected information for verification
            print(f'Paper title: {paper_title}')
            print(f'Paper ID: {paper_id}')
            print(f'Authors: {authors}')
            print(f'Journal Name and ID: {(journal_name, journal_id)}')
            print(f'Publication Year: {pub_year}')
            print('Codes:', codes)

            time.sleep(0.2)
            if (check_refs_exist()):
                time.sleep(0.4)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                time.sleep(0.2)
                spans = soup.find_all('a', href = True)
                time.sleep(0.2)
                for word in spans:
                    if (word.get_text()[0:2] == "MR" or word.get_text()[0:2] == "ar"):
                        listreferences.append(word.get_text())
                time.sleep(0.4)
            print("Done getting references for paper number " + str(paper_number) + " of " + prof + "\n", listreferences)
            data[prof]["Papers"][paper_id] = {
                "Title": paper_title,
                "PaperID": paper_id, 
                "Authors": authors,
                "Journal_Name": [journal_name, journal_id],
                "Publication_Year": pub_year,
                "References": listreferences,
                "Codes": codes}
        except:
            break


    with open(f'data/papers/{prof.replace(",","").replace(" ","").replace(".","")}_papers.json', 'w') as f:
        json.dump(data[prof], f)


    time.sleep(0.4)
    #go back to home
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(0.4)
    driver.get(toolsURL)
    time.sleep(0.4)
    print("Done searching for " + prof + "'s references \n")



# with open('data/papers/all_authors_papers.json', 'w') as f:
#     json.dump(data, f)



end_time = time.time()
total_time = end_time - start_time
hours, remainder = divmod(total_time, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Total run time: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")



