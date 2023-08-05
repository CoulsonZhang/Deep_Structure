from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import credential as c
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utilities as u
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


author_name = 'Ford, Kevin'


def setup_webdriver():
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

    return driver


author_ids = {}

def get_author_id(driver, name):
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

list_of_profs = ["Ford, Kevin B.",
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
"Guzman, Rosemary K.",
"Liu, Yuan",
"Quan, Zhiyu",
"Fadina, Tolulope",
"Rasmussen, Jacob",
"Rasmussen, Sarah Dean",
"Janda, Felix",
"Cooney, Daniel B",
"Hung, Pei-Ken",
"Young, Amanda",
"Wu, Xuan"]

driver = setup_webdriver()  
time.sleep(15)
for name in list_of_profs:
    author_ids[name] = get_author_id(driver, name)

with open('data/author_ids.json', 'w') as f:
    json.dump(author_ids, f)