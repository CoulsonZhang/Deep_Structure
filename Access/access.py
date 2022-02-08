import os
import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import credential as c

search_page = 'https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/index.html'
sample_page = 'https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/search/publications.html?pg4=AUCN&s4=kleinberg%2C+j*&co4=AND&pg5=AUCN&s5=&co5=AND&pg6=PC&s6=&co6=AND&pg7=ALLF&s7=&co7=AND&dr=all&yrop=eq&arg3=&yearRangeFirst=&yearRangeSecond=&pg8=ET&s8=All&review_format=html&Submit=Search'
full_sample = 'https://mathscinet-ams-org.proxy2.library.illinois.edu/mathscinet/search/publications.html?arg3=&co4=AND&co5=AND&co6=AND&co7=AND&dr=all&pg4=AUCN&pg5=AUCN&pg6=PC&pg7=ALLF&pg8=ET&review_format=html&s4=kleinberg%2C%20j%2A&s5=&s6=&s7=&s8=All&sort=Newest&vfpref=html&yearRangeFirst=&yearRangeSecond=&yrop=eq&r=1&extend=1'

class MR:
    def __init__(self):
        self.user = c.username;
        self.password = c.password;

        option = webdriver.ChromeOptions()
        option.add_argument("headless")
        base_path = os.path.dirname(os.path.abspath(__file__))
        drive_path = os.path.abspath(base_path + "/chromedriver")
        #driver = webdriver.Chrome(drive_path, options=option)
        driver = webdriver.Chrome(drive_path)

        self.driver = driver
        self.content  = None

    def clean(self):
        self.driver.quit()

    def login(self):
        driver = self.driver
        ## chance the search page url here
        driver.get(full_sample)
        time.sleep(0.2)
        driver.find_element_by_xpath("//*[@id='userNameInput']").click()
        time.sleep(0.2)
        driver.find_element_by_id("userNameInput").send_keys(self.user)
        time.sleep(0.2)
        driver.find_element_by_xpath("//*[@id='nextButton']").click()
        driver.find_element_by_id("passwordInput").send_keys(self.password)
        time.sleep(0.2)
        driver.find_element_by_xpath("//*[@id='submitButton']").click()
        # records = self.getRecord(driver)
        # return records


    def get_tittles(self):

        driver = self.driver
        time.sleep(0.2)
        content = driver.find_element_by_xpath("//*[@id='content']/form/div[3]/div[2]/div/div/div[17]/div[2]")
        print(content.text)
        # data = requests.get(sample_page)
        # print('HERE')
        # print(data)
        # content = BeautifulSoup(data.text, 'html.parser')
        # return content


if __name__ == '__main__':
    mr = MR()
    login = mr.login()
    mr.get_tittles()

    #If call login function, please remember to call clean after finishing
    #mr.clean()

    # data = requests.get(sample_page)
    # print('HERE')
    # print(data)
    # content = BeautifulSoup(data.text, 'html.parser')
    # print(content)
