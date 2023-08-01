import os
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import credential as c
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np
import re



from webdriver_manager.chrome import ChromeDriverManager


# list_of_profs = ["Ford, Kevin B.", "Tyson, Jeremy T."]

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
"Guzman, Rosemary K."]


# setup
option = webdriver.ChromeOptions()
toolsURL = "https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/index.html"
option.add_argument("headless")
#base_path = os.path.dirname(os.path.abspath(__file__))
#drive_path = os.path.abspath(base_path + "/chromedriver")
#driver = webdriver.Chrome(drive_path)
driver = webdriver.Chrome(ChromeDriverManager().install())

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
time.sleep(0.2)




profdict = {}


for professor in list_of_profs:
    time.sleep(0.2)
    driver.find_element_by_css_selector("input[type='radio'][value='pubyear']").click()
    time.sleep(0.2)
    select = Select(driver.find_element_by_id('yrop'))

    time.sleep(0.2)
    select.select_by_visible_text('>')
    time.sleep(0.3)
    driver.find_element_by_id("yearValue").send_keys("2010")
    time.sleep(0.4)
    driver.find_element_by_name("s4").send_keys(professor)
    time.sleep(0.4)

    driver.find_element_by_name("Submit").click()
    time.sleep(0.4)

    driver.find_element_by_class_name("mrnum").click()

    time.sleep(0.2)

    lnks=driver.find_elements_by_tag_name("a")

    time.sleep(0.2)
    # traverse list
    codes =[]
    for lnk in lnks:
        if ((lnk.get_attribute('href') is not None) and ('https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/search/mscdoc.html?code=' in lnk.get_attribute('href'))):
            code = lnk.get_attribute('href').replace('https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/2006/mathscinet/search/mscdoc.html?code=', '')
            codes.append(code)
        time.sleep(0.2)
    
    while (True):
        time.sleep(0.2)
        try: 
            driver.find_element_by_partial_link_text("Next").click()
            time.sleep(0.2)
            lnks=driver.find_elements_by_tag_name("a")
            time.sleep(0.1)
            # traverse list
            for lnk in lnks:
                if ((lnk.get_attribute('href') is not None) and ('https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/search/mscdoc.html?code=' in lnk.get_attribute('href'))):
                    time.sleep(0.2)
                    code = lnk.get_attribute('href').replace('https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/search/mscdoc.html?code=', '')
                    time.sleep(0.2)
                    codes.append(code)
            time.sleep(0.2)
        except:
            break

    time.sleep(0.2)
    new_list = []
    pattern = '(.*?)'+','+'\\(' + '(.*?)' + '\\)'
    for i in range(len(codes)):
        actual_list = []
        code2 = codes[i]
        matchObj = re.search(pattern,code2, re.M|re.I)
        if matchObj:
            primary_classification = matchObj.group(1)
            actual_list.append(primary_classification)
            within_par = matchObj.group(2)
            if ("," in within_par):
                new_list1 = within_par.split(",")
                for i in range(len(new_list1)):
                    actual_list.append(new_list1[i])
            else:
                actual_list.append(within_par)
        else:
            actual_list.append(codes[i])
        new_list.append(actual_list)
    profdict[professor] = new_list
    time.sleep(0.1)
    driver.find_element_by_link_text("Home").click()
    time.sleep(0.1)

    






print(profdict)

df = pd.DataFrame.from_dict(profdict.items())
df.columns = ['Keys', 'Values']

df.to_csv("classification_info.csv")

# pd.DataFrame.from_dict(profdict, orient='index', columns=['Values']).to_csv("classification_info.csv")


    
driver.quit()