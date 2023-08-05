from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import credential as c
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utilities as u
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException



option = webdriver.ChromeOptions()
toolsURL = "https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/index.html"
option.add_argument("headless")
driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install())


def get_author_name(name):
    # Desired URL
    desired_url = "https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/index.html"
    print("Finding author name for " + name + "...")
    try:
        # Wait until URL is the desired URL
        WebDriverWait(driver, 50).until(lambda d: d.current_url == desired_url)
    except TimeoutException:
        print("Loading took too much time!-Try again")
        return None

    url = 'https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/search/authors.html?authorName={}&Submit=Search'.format(name)
    time.sleep(3)

    driver.execute_script("window.open('');")

    driver.switch_to.window(driver.window_handles[1])

    driver.get(url)

    time.sleep(5)
    try:
        result_name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.authorName.important"))
        )
        #print(result_name.text)
        result_text = result_name.text
    except:
        print(name)
        print("Multiple name possible, please re-check your input")
        result_text = None

    driver.close()

    driver.switch_to.window(driver.window_handles[0])
    print(f"Done finding name for {name} \n")
    return result_text



def fetch_title(url):
    print("fetching title...")
    time.sleep(5)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    time.sleep(5)

    titles = []

    heads = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.headline"))
    )

    for head in heads:
        # fetch the title in this paper
        title = head.find_element_by_css_selector('span.title').text
        titles.append(title)

    print("Check/Go next page")

    driver.close()

    driver.switch_to.window(driver.window_handles[0])
    print("Done fetching title \n")
    return titles


def fetch_single_title(url):
    print("fetching single title...")
    time.sleep(5)
    driver.execute_script("window.open('');")
    time
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    time.sleep(5)

    title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.title"))
    )
            
    title = title_element.text

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("Done fetching single title \n")
    return [title]


def get_author_id(name):
    print("Getting author ID for " + name + "...")
    url = 'https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/search/authors.html?authorName={}&Submit=Search'.format(name)
    
    time.sleep(5)
    driver.execute_script("window.open('');")

    driver.switch_to.window(driver.window_handles[1])

    driver.get(url)
    time.sleep(3)
    identify = driver.title.split(' ')[-1].strip()

    print("title is " + driver.title)
    print(f"author ID for {name} is " + identify)

    driver.close()

    driver.switch_to.window(driver.window_handles[0])
    print("Done getting author ID \n")
    return identify



def fetch_citation(url):
    print("fetching citation...")

    driver.get(url)
    time.sleep(5)
    cite = {}  # dict for storing the paper citation page (for citation)

    heads = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.headline"))
    )

    for head in heads:
        # fetch the title in this paper
        title = head.find_element_by_css_selector('span.title').text

        print('processing paper for fetch_citation: {}'.format(title))

        # fetch the url for detail page & citation page
        citation = head.find_element_by_css_selector('div.headlineMenu')
        menu_links = citation.find_elements_by_css_selector('a')

        last_link_text = menu_links[-1].text
        print(last_link_text + "\n")
        citation_page = menu_links[-1].get_attribute('href')
                    
        if "Citations" in last_link_text:
            cite[title] = fetch_title(citation_page)
            print(fetch_title(citation_page))
            print("multiple citation \n")
        elif "Citation" in last_link_text:
            cite[title] = fetch_single_title(citation_page)
            print(fetch_single_title(citation_page))
            print("single citation \n")
        else:
            cite[title] = None

    print("Check/Go next page")
    print("Done fetching citation \n \n")
    return cite



def search(name):
    first = 'https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/search/publications.html?pg4=AUCN&s4='
    second = '&co4=AND&pg5=TI&s5=&co5=AND&pg6=PC&s6=&co6=AND&pg7=SE&s7=&co7=ANDdr=pubyear&yrop=gt&arg3=2010&yearRangeFirst=&yearRangeSecond=&pg8=ET&s8=All&review_format=pdf&Submit=Search'
    return first + name + second


