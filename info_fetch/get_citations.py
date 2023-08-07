from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import credential as c
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import re
import time
start_time = time.time()

# setup
option = webdriver.ChromeOptions()
toolsURL = "https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/index.html"
option.add_argument("headless")
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

time.sleep(0.5)

driver.find_element_by_xpath("//*[@id='idSIButton9']").click()
time.sleep(5)


def check_exists_by_partial_link_text():
    try:
        element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Next")))
        return True
    except:
        return False
from selenium.common.exceptions import TimeoutException

def fetch_title(url):
    print("fetching title...")
    time.sleep(1)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    paper_id_from_title = soup.title.string
    result = re.search(r"(\d+)", paper_id_from_title)

    mr_number = None
    if result:
        mr_number = "MR" + result.group(1)
    print("Fetching citations for paper with ID:")
    print(mr_number)
    
    titles = []

    while True:
        heads = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.headline"))
        )

        for head in heads:
            # fetch the title in this paper
            title_element = head.find_element_by_css_selector('span.title')
            title = title_element.text if title_element else None

            # fetch the MR number in this paper
            mrnum_element = head.find_element_by_css_selector('strong')
            mrnum_of_cite = mrnum_element.text if mrnum_element else None

            titles.append((title, mrnum_of_cite))

        try:
            wait = WebDriverWait(driver, 1.5)
            next_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Next")))
            next_link.click()
            time.sleep(1)
        except TimeoutException:
            break

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("Done fetching title \n")
    return titles



def fetch_single_title(url):
    print("fetching single title...")
    time.sleep(1)
    driver.execute_script("window.open('');")
    time
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    time.sleep(1)


    soup = BeautifulSoup(driver.page_source, 'html.parser')
    paper_id_from_title = soup.title.string
    result = re.search(r"(\d+)", paper_id_from_title)

    mr_number = None
    if result:
        mr_number = "MR" + result.group(1)
    print("Fetching citations for paper with ID:")
    print(mr_number)


    title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.title"))
    )
            

    title = title_element.text

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    headline_div = soup.find('div', class_='headline')

    mrnum_element = headline_div.find('strong') if headline_div else None

    mrnum_of_cite = mrnum_element.string if mrnum_element else None

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("Done fetching single title \n")
    return [(title,mrnum_of_cite)]


def fetch_citation(url):
    print("fetching citation...")
    WebDriverWait(driver, timeout=30).until(lambda d: d.current_url.startswith("https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/"))

    driver.get(url)
    time.sleep(1)


    cite = {}  # dict for storing the paper citation page (for citation)

    heads = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.headline"))
    )

    for head in heads:
        # fetch the title in this paper
        title = head.find_element_by_css_selector('span.title').text

        # fetch the MR number
        mrnum_element = head.find_element_by_css_selector('a.mrnum')
        mrnum = mrnum_element.text.strip()
        paper_current = (title, mrnum)
        
        print('processing paper for fetch_citation: {}'.format(title))

        # fetch the url for detail page & citation page
        citation = head.find_element_by_css_selector('div.headlineMenu')
        menu_links = citation.find_elements_by_css_selector('a')

        last_link_text = menu_links[-1].text
        print(last_link_text + "\n")
        citation_page = menu_links[-1].get_attribute('href')
                    
        if "Citations" in last_link_text:
            cite[mrnum] = fetch_title(citation_page)
            print("Detected multiple citations \n")
        elif "Citation" in last_link_text:
            cite[mrnum] = fetch_single_title(citation_page)
            print("Detected single citation \n")
        else:
            cite[mrnum] = None
        time_elapsed = time.time() - start_time
        print(f'Time elapsed so far: {time_elapsed/60} minutes')
    print("Done fetching citation \n \n")
    return cite



def search_for_pubs(authorID):
    return "https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/search/publications.html?pg1=INDI&s1="+authorID+"&sort=Newest&vfpref=pdf&r=1&extend=1"

#author_ID_for_search = '1054758' #Felix Leditzky

#Sheldon Katz pubs URL: https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/search/publications.html?pg1=INDI&s1=198078&sort=Newest&vfpref=pdf&r=1&extend=1



path = os.getcwd()

with open(path + '/data/author_ids.json', 'r') as f:
    data = json.load(f)


# for author_name, author_ID in data.items():
#     cite = fetch_citation(search_for_pubs(author_ID))
#     with open(f'data/citations/{author_name.replace(" ", "").replace(".","").replace(",","")}_citations.json', 'w') as f:
#         json.dump(cite, f)


cite = fetch_citation(search_for_pubs("1216581"))
with open(f'data/citations/{"Wei, Wei".replace(" ", "").replace(".","").replace(",","")}_citations.json', 'w') as f:
    json.dump(cite, f)


end_time = time.time()
total_time = end_time - start_time
hours, remainder = divmod(total_time, 3600)
minutes, seconds = divmod(remainder, 60)

print(f"Total run time: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds")

