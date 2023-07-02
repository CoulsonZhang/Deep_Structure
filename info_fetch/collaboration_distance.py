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


from webdriver_manager.chrome import ChromeDriverManager

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





# go to collaboration tools section 
driver.find_element_by_id("tab2link").click()
time.sleep(0.2)

 

def collaboration_distance(author1, author2):
    time.sleep(0.2)
    try:
        element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "AuthorSourceName"))
    )
    except:
        driver.quit()
    driver.find_element_by_id("AuthorSourceName").send_keys(author1)
    time.sleep(0.2)
    search2 = driver.find_element_by_id("AuthorTargetName")
    time.sleep(0.2)
    search2.send_keys(author2)
    time.sleep(0.2)
    search2.send_keys(Keys.RETURN)
    time.sleep(0.2)
    
    
    

    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "erdosNumber"))
    )
    except:
        driver.quit()

    time.sleep(0.2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    spans = soup.find_all('span', {'class' : 'erdosNumber'})

    distance = spans[0].get_text()
    

    # go back to original search
    time.sleep(0.2)
    link = driver.find_element_by_css_selector('[value="New Search"]')
    time.sleep(0.2)
    link.click()
    time.sleep(0.2)

    return int(distance[27:len(distance)])


df = pd.read_csv("namesofprofessors.csv")
faculty = df['professornames'].tolist()
matrix = np.zeros((len(faculty), len(faculty)))

for i in range(len(faculty) - 1):
    time.sleep(0.2)
    for j in range(i + 1, len(faculty)):
        time.sleep(0.2)
        matrix[i][j] = collaboration_distance(faculty[i], faculty[j])


pd.DataFrame(matrix).to_csv("faculty_collaboration_distance.csv")


