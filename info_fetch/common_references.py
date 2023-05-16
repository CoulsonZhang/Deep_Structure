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

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


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
toolsURL = "https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/index.html"
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
#try:
#    element = WebDriverWait(driver, 15).until(
#    EC.presence_of_element_located((By.NAME, "s4"))
#)
#except:
#    driver.quit()
#time.sleep(0.3)


#check if there is next paper
def check_exists_by_partial_link_text():
    try:
        driver.find_element_partial_link_text("Next")
    except:
        return False
    return True

#check if there is reference list for each author
def check_exists_by_class_name():
    try:
        driver.find_element_by_class_name("reflist")
    except:
        return False
    return True


profdict = {}

for proffessor in list_of_profs:
    #enter information (professor name and starting year)
    time.sleep(0.4)
    try:
        element = WebDriverWait(driver, 10).until(
           EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio'][value='pubyear']"))
        )
        element.click()
    except:
        print("Element not found")
    time.sleep(0.4)
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yrop')))
        select = Select(driver.find_element_by_id('yrop'))
        select.select_by_visible_text('>')
    except Exception as e:
        print("Error while selecting from dropdown: ", e)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'yearValue')))
        driver.find_element_by_id("yearValue").send_keys("2010")
    except Exception as e:
        print("Error while entering year: ", e)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 's4')))
        driver.find_element_by_name("s4").send_keys(proffessor)
    except Exception as e:
        print("Error while entering professor name: ", e)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'Submit')))
        driver.find_element_by_name("Submit").click()
    except Exception as e:
        print("Error while clicking submit: ", e)

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'mrnum')))
        driver.find_element_by_class_name("mrnum").click()
    except Exception as e:
        print("Error while clicking on mrnum: ", e)

    # get all references for all paper for one author
    listreferences = []
    time.sleep(0.2)
    if (check_exists_by_class_name()):
        soup = BeautifulSoup(driver.page_source, "html.parser")
        spans = soup.find_all('a', href = True)
        for word in spans:
            if (word.get_text()[0:2] == "MR" or word.get_text()[0:2] == "ar"):
                listreferences.append(word.get_text())

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
                for word in spans:
                    if (word.get_text()[0:2] == "MR" or word.get_text()[0:2] == "ar"):
                        listreferences.append(word.get_text())
                time.sleep(0.4)
        except:
            break
    #dictionary with key professor and value of all of their references
    profdict[proffessor] = listreferences
    time.sleep(0.4)

    #go back to home
    driver.find_element_by_link_text("Home").click()
    time.sleep(0.4)



df = pd.read_csv("namesofprofessors.csv")
faculty = df['professornames'].tolist()

#returns length of the intersection of two reference lists of two authors
def common_reference(author1, author2):
    listOne = profdict.get(list_of_profs[faculty.index(author1)])
    listTwo = profdict.get(list_of_profs[faculty.index(author2)])

    lengthNumber = len(list(set(listOne).intersection(set(listTwo))))
    return lengthNumber


matrix = np.zeros((len(faculty), len(faculty)))

for i in range(len(faculty)):
    for j in range(len(faculty)):
        matrix[i][j] = common_reference(faculty[i], faculty[j])


#convert matrix to csv file
pd.DataFrame(matrix).to_csv("common_references.csv")

print(len(list_of_profs))
print(len(faculty))
