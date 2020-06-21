from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from login_info import MAIL, PASSWORD
from scrape_page import WebPage
import pickle


class LikenBot():
    """Represents a LinkedIn url profile scraper bot.

        Contains methods:
            __init__ to set variables and validate the user's choice of job and location to scrape
            login function to connect on Linkedin web site
            scrap_url_profile function to scrape every valid url profile
            save_result function to dump the scrape data to a pickle file
            load_result function to load the scrape data to a pickle file

        Contains class constants:
            PREFIX = "https://www.linkedin.com/in/"
     """

    PREFIX = "https://www.linkedin.com/in/"

    def __init__(self, job="data scientist", location="Tel-Aviv", nb_page=2):

        """ Initializes the LikenBot class. Also initializes the Selenium driver for scraping the webpage
            and the dictionaries that contains the results

            Parameters:
                job (str): To looking for linkedin profile with this job, initialize to "data scientist"
                location (str): To looking for linkedin profile in this location, initialize to "Tel-Aviv"
                nb_page (int): Number of google pages we want to scrape to extract profile url
            """

        self.driver = webdriver.Chrome()
        # initialize data
        self.url_dic = {}
        self.final_dic_result = {}
        self.job = job
        self.location = location
        self.nb_page = nb_page

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
        """ The function will scrape linkedin url profile on google"""
        self.driver.get('https://www.google.com/')

        # the search bar to input query
        query = self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')

        # the query we put in the google browser
        query.send_keys(f'site:linkedin.com/in/ AND "{self.job}" AND "{self.location}"')
        query.send_keys(Keys.RETURN)
        sleep(1)

        for i in range(self.nb_page):

            # contain second part of the url of all the profile of the page in list
            linkedin_urls = self.driver.find_elements_by_class_name('eipWBe')

            # create our valid url without '...' and with length > 0 and save it in url_dic
            for url in linkedin_urls:
                if len(url.text) != 0 and url.text[-3:] != '...':
                    if self.PREFIX + url.text[2:] + '/' not in self.url_dic:
                        self.url_dic[self.PREFIX + url.text[2:] + '/'] = 1

            # Try to click on google next page to scrap new profile until possible
            try:
                next_btn = self.driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
                next_btn.click()
                sleep(2)

            except:
                print('No more clickable')
                break

        # the list of all the linkedin scrape profile url
        list_of_url = self.url_dic.keys()

        # Loop on the url linkedin profile, to scrape data on it using the class WebPage from scrape_page.py
        for url_profile in list_of_url:
            try:
                sleep(1)
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

    def load_result(self):
        """The function load our result from the pickle file"""

        dbfile = open('profile_pickle', 'rb')
        db = pickle.load(dbfile)
        print(db)
        dbfile.close()


if __name__ == '__main__':
    bot = LikenBot()
    bot.login()
    bot.scrap_url_profile()
    bot.save_result()
    bot.load_result()
