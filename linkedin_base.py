from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from scrape_page import WebPage
import pickle
import pprint
from constants import *

class LinkedinBot:
    """Represents a LinkedIn url profile scraper bot.

        Contains methods:
            __init__ to set variables and validate the user's choice of job and location to scrape
            login function to connect on Linkedin web site
            scrape_url_profile function to scrape every valid url profile
            save_result function to dump the scrape data to a pickle file
            load_result function to load the scrape data to a pickle file

        uses constants:

     """



    def __init__(self, email,password,sections,job="data scientist", location="Tel Aviv", nb_pages=2):

        """ Initializes the LinkedinBot class. Also initializes the Selenium driver for scraping the webpage
            and the dictionaries that contains the results

            Parameters:
                job (str): To looking for linkedin profile with this job, initialize to "data scientist"
                location (str): To looking for linkedin profile in this location, initialize to "Tel-Aviv"
                nb_page (int): Number of google pages we want to scrape to extract profile url
            """
        self.email=email
        self.password=password
        self.driver = webdriver.Chrome()
        # initialize data
        self.url_dic = {}
        self.scraped_page_data = {}
        self.job = job
        self.location = location
        self.nb_pages = nb_pages
        self.sections=sections

    def login(self):
        """ This function logs in to the LinkedIn web site"""
        self.driver.get(LINKEDIN_MAIN_URL)

        # Ask LinkedIn to let us log in
        login_btn_1 = self.driver.find_element_by_xpath(ASK_LOGIN_XPATH)
        login_btn_1.click()

        sleep(CLICK_WAIT_TIME)

        # Enter email address as username
        email_in = self.driver.find_element_by_xpath(USER_NAME_XPATH)
        email_in.send_keys(self.email)

        # enter the password
        pw_in = self.driver.find_element_by_xpath(PASSWORD_XPATH)
        pw_in.send_keys(self.password)

        # log in to the website
        login_btn_2 = self.driver.find_element_by_xpath(LOGIN_BUTTON_XPATH)
        login_btn_2.click()

    def scrape_url_profiles(self):
        """ This function searches google for profiles on LinkedIn
        that match the search terms given by the user"""
        self.driver.get(GOOGLE_URL)

        # the search bar to input query
        query = self.driver.find_element_by_xpath(GOOGLE_SEARCH_BAR_XPATH)

        # Search google for our search terms in the google browser
        query.send_keys(GOOGLE_SEARCH_STRING.format(self.job,self.location))
        query.send_keys(Keys.RETURN)
        sleep(CLICK_WAIT_TIME)

        for i in range(self.nb_pages):

            # Find links that correspond to search results
            linkedin_urls = self.driver.find_elements_by_class_name(CORRECT_GOOGLE_RESULT_ID)

            # Find valid urls by ensuring they do not contain '...' and have length > 0
            # If they are not already in the url_dic, save them in url_dic
            for url in linkedin_urls:

                if len(url.text) != 0 and url.text[URL_END_INDEX:] != '...':
                    cur_url=LINKEDIN_PREFIX + url.text[URL_START_INDEX:] + '/'
                    if cur_url not in self.url_dic:
                        self.url_dic[cur_url] = 1

            # Try to click on next google page to scrape new profile until it becomes impossible
            try:
                next_btn = self.driver.find_element_by_xpath(GOOGLE_NEXT_PAGE)
                next_btn.click()
                sleep(CLICK_WAIT_TIME*2)

            except:
                print('Unable to search for any more profiles')
                break

        # Get the list of all the LinkedIn profiles
        list_of_urls = self.url_dic.keys()
        print(NUM_PROFILES_FOUND.format(len(list_of_urls)))
        # Loop over all urls to scrape data on it using the class WebPage from scrape_page.py
        for url_profile in list_of_urls:
            try:
                sleep(CLICK_WAIT_TIME)
                this_url = WebPage(url_profile, self.driver,self.sections)
                this_url.get_data()
                self.scraped_page_data.update(this_url.export_data())


            except Exception as ex:
                print(PAGE_SCRAPE_FAILED_ERROR.format(ex,url_profile))
                print("Moving on to next profile")
                continue

        self.driver.close()

    def save_result(self):
        """The function saves our result in a pickle file"""

        dbfile = open(PICKLE_FILENAME, 'wb')
        pickle.dump(self.scraped_page_data, dbfile)
        dbfile.close()

    def load_result(self):
        """The function loads our result from the pickle file"""

        dbfile = open(PICKLE_FILENAME, 'rb')
        db = pickle.load(dbfile)
        pprint.pprint(db)
        dbfile.close()

if __name__ == '__main__':
    bot = LinkedinBot(nb_pages=10)
    bot.login()
    bot.scrape_url_profiles()
    bot.save_result()
    bot.load_result()
