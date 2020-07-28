from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.chrome.options import Options
from scrape_page import WebPage
import pickle
import pprint
from university_api import UniversityAPI
from constants import *

from linkedin_logger import getmylogger

logger = getmylogger(__name__)


class LinkedinBot:
    """Represents a LinkedIn url profile scraper bot.

        Contains methods:
            __init__ to set variables and validate the user's choice of job and location to scrape
            login function to connect on Linkedin web site
            get_profile_urls function to find every valid url profile
            scrape_content_profiles to scrape data from those urls
            export_scrapes function to dump scrape data to the logger
            save_result function to dump the scrape data to a pickle file
            load_result function to load the scrape data to a pickle file

        uses constants:

     """

    def __init__(self, email, password, sections, database, job="data scientist", location="Tel Aviv", nb_pages=2):

        """ Initializes the LinkedinBot class. Also initializes the Selenium driver for scraping the webpage
            and the dictionaries that contains the results

            Parameters:
                job (str): To looking for linkedin profile with this job, initialize to "data scientist"
                location (str): To looking for linkedin profile in this location, initialize to "Tel-Aviv"
                nb_page (int): Number of google pages we want to scrape to extract profile url
            """
        self.email = email
        self.password = password
        chrome_options=Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        # initialize data
        self.url_dic = {}
        self.scraped_page_data = {}
        self.job = job
        self.location = location
        self.nb_pages = nb_pages
        self.sections = sections
        self.db_bot = database
        self.api = UniversityAPI()

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
        logger.info(SUCCESSFULLY_LOGGED_IN)

    def get_profile_urls(self):
        """ This function searches google for profiles on LinkedIn
        that match the search terms given by the user"""
        self.driver.get(GOOGLE_URL)

        # the search bar to input query
        query = self.driver.find_element_by_xpath(GOOGLE_SEARCH_BAR_XPATH)

        # Search google for our search terms in the google browser
        query.send_keys(GOOGLE_SEARCH_STRING.format(self.job, self.location))
        query.send_keys(Keys.RETURN)
        sleep(CLICK_WAIT_TIME)
        logger.info(SEARCHED_GOOGLE.format(self.job, self.location))
        for page in range(self.nb_pages):

            # Find links that correspond to search results

            linkedin_urls = self.driver.find_elements_by_class_name(CORRECT_GOOGLE_RESULT_ID)

            # Find valid urls by ensuring they do not contain '...' and have length > 0
            # If they are not already in the url_dic, save them in url_dic
            for url in linkedin_urls:

                if len(url.text) != 0 and url.text[URL_END_INDEX:] != '...':
                    cur_url = LINKEDIN_PREFIX + url.text[URL_START_INDEX:] + '/'
                    if cur_url not in self.url_dic:
                        self.url_dic[cur_url] = 1

            # Try to click on next google page to scrape new profile until it becomes impossible
            try:
                next_btn = self.driver.find_element_by_xpath(GOOGLE_NEXT_PAGE)
                next_btn.click()
                sleep(CLICK_WAIT_TIME * 2)

            except:
                logger.warning(NO_MORE_PROFILES_MESSAGE)
                break

    def scrape_content_profiles(self):

        # Get the list of all the LinkedIn profiles
        list_of_urls = self.url_dic.keys()
        logger.info(NUM_PROFILES_FOUND.format(len(list_of_urls)))

        # Don't scrape urls that are already in the database
        if len(self.db_bot.old_urls) > 0:
            list_of_urls = [url for url in list_of_urls if url not in self.db_bot.old_urls]
            logger.info(NUM_NEW_PROFILES_FOUND.format(len(list_of_urls)))
        # Loop over all urls to scrape data on it using the class WebPage from scrape_page.py
        successful_scrapes = 0
        for url_profile in list_of_urls:
            logger.info(PROFILE_SCRAPING_MESSAGE.format(url_profile))
            try:
                sleep(CLICK_WAIT_TIME)
                this_url = WebPage(url_profile, self.driver, self.sections)
                this_url.get_data()
                self.scraped_page_data.update(this_url.export_data())
            except Exception as ex:
                logger.error(PAGE_SCRAPE_FAILED_ERROR.format(ex, url_profile))
                continue
            else:
                successful_scrapes += 1
            try:
                api_result = {}
                self.api.get_new_universities(this_url.export_data())
                if len(self.api.update_list) > 0:
                    self.api.get_data_from_api()
                    api_result = self.api.return_api_data()

            except Exception as ex:
                logger.error(API_GOT_ERROR.format(ex))
            try:

                self.db_bot.insert_experience(dic_scrap_profile=this_url.export_data())
                self.db_bot.insert_education(dic_scrap_profile=this_url.export_data(), api_result=api_result)
                self.db_bot.insert_skills(dic_scrap_profile=this_url.export_data())
            except Exception as ex:
                logger.error(FAILED_SECTION_INSERT.format(ex))
            else:
                logger.debug(PAGE_DATA_ADDED_DB.format(url_profile))
        logger.info(SUCCESSFUL_SCRAPES_DONE.format(successful_scrapes))
        self.driver.close()
        self.db_bot.close()

    def export_scrapes(self):
        """Exports the final dictionary and the data from the API to the logger"""
        my_dict = self.scraped_page_data
        api_data = self.api.extract_api_data()
        linkedin_print = pprint.pformat(my_dict)
        logger.debug(linkedin_print)
        api_print = pprint.pformat(api_data)
        logger.debug(api_print)

    def save_result(self):
        """The function saves our result in a pickle file"""

        dbfile = open(DEFAULT_PICKLE_FILENAME, 'wb')
        pickle.dump(self.scraped_page_data, dbfile)
        dbfile.close()

    def load_result(self):
        """The function loads our result from the pickle file"""

        dbfile = open(DEFAULT_PICKLE_FILENAME, 'rb')
        db = pickle.load(dbfile)
        database_print = pprint.pformat(db)
        logger.debug(database_print)
        dbfile.close()
