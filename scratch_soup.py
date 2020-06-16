
import requests
from bs4 import BeautifulSoup
from collections import Counter
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import json

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
#myresult=driver.get("https://www.linkedin.com/in/chris-lindner-170a0385/")
driver.get('https://www.linkedin.com/in/williamhgates/')
SCROLL_PAUSE_TIME=1
driver.execute_script("document.body.style.zoom='10%'")
driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
sleep(SCROLL_PAUSE_TIME)
driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")
#while True:
    # Scroll down to bottom

    # Calculate new scroll height and compare with last scroll height
#    new_height = driver.execute_script("return document.body.scrollHeight")
#    if new_height == last_height:
#        break
#    last_height = new_height

experience=driver.find_elements_by_xpath('//*[@id = "experience-section"]//ul//li')
for item in experience:
    print(item)
    print("")

education=driver.find_elements_by_xpath('//*[@id = "education-section"]//ul//li')
for item in education:
    print(item.text)
    print("")

featured=driver.find_elements_by_xpath('//*[contains(class, "pab-featured_section"]//ul//li')
for item in education:
    print(item.text)
    print("")
#experience= driver.find_element_by_id("experience-section")
#//ul[contains(@class,"section-info")]')
#

#with open('web_structure.txt', 'w', encoding="utf-8") as pass_file:
#    pass_file.write(soup.prettify())
#print(soup.get_text)

if __name__=="__main__":



    print("All tests passed")