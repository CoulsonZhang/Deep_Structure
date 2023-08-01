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
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import url_to_be



option = webdriver.ChromeOptions()
toolsURL = "https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/index.html"
option.add_argument("headless")
driver = webdriver.Chrome(ChromeDriverManager(version="114.0.5735.90").install())
driver.get(toolsURL)
time.sleep(1)

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


with open('data/author_ids.json', 'r') as f:
    author_ids = json.load(f)



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
"Tzirakis, Nikolaos",
"Kerman, Ely",
"Di Francesco, Philippe",
"Laugesen, Richard Snyder",
"Heller, Jeremiah Ben",
"Guzman, Rosemary K.",
"Jing, Xiaochen",
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

dict_of_coauthors = {}

for prof in list_of_profs:
    print("Now searching for coauthors of " + prof)
    author_id = None
    
    if prof in author_ids:
        author_id = author_ids[prof]
        print("Found ID for " + prof + ": " + author_id)
    else:
        print(f"No ID found for {prof}. Skipping.")
        continue
    
    url = f"https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/search/authors.html?coauth={author_id}&sort=&r=1&extend=1"

    time.sleep(2)
    
    WebDriverWait(driver, timeout=30).until(url_to_be(toolsURL))

    if driver.current_url == toolsURL:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(2)

    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'a')))
        a_elements = driver.find_elements_by_tag_name('a')
        coauthor_ids = [(a.text, a.get_attribute('href').split('=')[-1]) for a in a_elements if 'mrauthid' in a.get_attribute('href')]

    except Exception as e:
        print("Error while extracting coauthor IDs: ", e)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    

    dict_of_coauthors[prof] = coauthor_ids


with open('data/dict_of_coauthors.json', 'w') as f:
    json.dump(dict_of_coauthors, f)


