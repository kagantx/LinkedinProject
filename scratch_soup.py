
import requests
from bs4 import BeautifulSoup
from collections import Counter
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import pprint
import json
from scrapewebpage import WebPage
driver=webdriver.Chrome()

page=driver.get("http://www.linkedin.com/")

    # identification button
login_btn_1 = driver.find_element_by_xpath('/html/body/nav/a[3]')
login_btn_1.click()

sleep(1)

email_in = driver.find_element_by_xpath('//*[@id="username"]')
with open('user_name.txt', 'r') as email_file:
    email = email_file.readline().strip()
email_in.send_keys(email)

pw_in = driver.find_element_by_xpath('//*[@id="password"]')
with open('password.txt', 'r') as pass_file:
    password = pass_file.readline().strip()
pw_in.send_keys(password)

login_btn_2 = driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button')
login_btn_2.click()
#myresult=driver.get(")
this_page=WebPage(r"https://www.linkedin.com/in/lucas-bensaid-898ab8130/",driver)
this_page.get_data()
#while True:
    # Scroll down to bottom

    # Calculate new scroll height and compare with last scroll height
#    new_height = driver.execute_script("return document.body.scrollHeight")
#    if new_height == last_height:
#        break
#    last_height = new_height


if __name__=="__main__":



    print("All tests passed")