from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from login_info import MAIL, PASSWORD
from scrape_page import WebPage
import pickle

PREFIX = "https://www.linkedin.com/in/"


class LikenBot():
    def __init__(self):
        """The function initialize our class as the chrome web page"""
        self.driver = webdriver.Chrome()
        self.url_dic = {}
        self.final_dic_result = {}

    def login(self):
        """ The function login inside the Linkedin web site"""
        self.driver.get('https://www.linkedin.com/')

        # identification button
        login_btn_1 = self.driver.find_element_by_xpath('/html/body/nav/a[3]')
        login_btn_1.click()

        sleep(1)

        # enter the mail
        email_in = self.driver.find_element_by_xpath('//*[@id="username"]')
        email_in.send_keys(MAIL)

        # enter the password
        pw_in = self.driver.find_element_by_xpath('//*[@id="password"]')
        pw_in.send_keys(PASSWORD)

        # connect button
        login_btn_2 = self.driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button')
        login_btn_2.click()

    def scrap_url_profile(self):
        """ The function will scrape url profile of data scientist on google"""
        self.driver.get('https://www.google.com/')

        # the search bar to input query
        query = self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')

        # the query we put in the google browser (could be change by hand if we change localisation or ...)
        query.send_keys('site:linkedin.com/in/ AND "data scientist" AND "Tel-Aviv"')

        # .send_keys() to simulate the return key
        query.send_keys(Keys.RETURN)
        sleep(1)

        """ CHANGE FOR TO WHILE FOR LONGEST LOOP"""
        # while True:
        for i in range(1):

            # contain second part of the url of all the profile of the page in list
            linkedin_urls = self.driver.find_elements_by_class_name('eipWBe')

            # create our url avoiding duplicate and the wrong one
            for url in linkedin_urls:
                if len(url.text) != 0 and url.text[-3:] != '...':
                    if PREFIX + url.text[2:] + '/' not in self.url_dic:
                        self.url_dic[PREFIX + url.text[2:] + '/'] = 1

            # click on the next page to scrap new profile until possible
            try:
                next_btn = self.driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
                next_btn.click()
                sleep(2)

            except:
                print('No more clickable')
                break

        # the list of all the scrap profile url
        list_of_url = self.url_dic.keys()

        # Loop on the url to scrap it using the class WebPage from scrape_page.py
        for url_profile in list_of_url:
            try:
                sleep(1)

                """ SCRAP THE PROFILE -> DANIEL FUNCTION"""
                my_class = WebPage(url_profile, self.driver)
                my_class.get_data()
                self.final_dic_result.update(my_class.export_data())


            except:
                continue

        self.driver.close()

    def save_result(self):
        """The function saves our result in a pickle file"""

        dbfile = open('profile_pickle', 'wb')
        pickle.dump(self.final_dic_result, dbfile)
        dbfile.close()


if __name__ == '__main__':
    bot = LikenBot()
    bot.login()
    bot.scrap_url_profile()
    bot.save_result()
