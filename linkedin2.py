from telnetlib import EC

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import lxml
import requests
from bs4 import BeautifulSoup


class LikenBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get('https://www.linkedin.com/')

        # identification button
        login_btn_1 = self.driver.find_element_by_xpath('/html/body/nav/a[3]')
        login_btn_1.click()

        sleep(1)

        email_in = self.driver.find_element_by_xpath('//*[@id="username"]')
        email_in.send_keys('bensaid.lucas@gmail.com')

        pw_in = self.driver.find_element_by_xpath('//*[@id="password"]')
        pw_in.send_keys('261194')

        login_btn_2 = self.driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button')
        login_btn_2.click()

    def url_profile(self):
        self.driver.get('https://www.google.com/')

        query = self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
        query.send_keys('site:linkedin.com/in/ AND "data scientist" AND "Tel-Aviv"')
        # .send_keys() to simulate the return key
        query.send_keys(Keys.RETURN)

        url = []
        # to change if we change localisation
        PREFIX = "il.linkedin.com/in/"

        # while True:
        for i in range(5):

            linkedin_urls = self.driver.find_elements_by_class_name('eipWBe')

            url.append([PREFIX + url.text[2:] for url in linkedin_urls if
                        len(url.text) != 0 and url.text[-3:] != '...'])

            try:
                next_btn = self.driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]').click()
                sleep(2)

            except:
                print('no more clickable')
                break

        print(url)


if __name__ == '__main__':
    bot = LikenBot()
    bot.login()
    bot.url_profile()
