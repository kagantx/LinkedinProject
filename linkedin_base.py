from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from scrape_page import WebPage
import pickle
import pprint
import sqlite3
import os
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

    def __init__(self, email, password, sections, job="data scientist", location="Tel Aviv", nb_pages=2):

        """ Initializes the LinkedinBot class. Also initializes the Selenium driver for scraping the webpage
            and the dictionaries that contains the results

            Parameters:
                job (str): To looking for linkedin profile with this job, initialize to "data scientist"
                location (str): To looking for linkedin profile in this location, initialize to "Tel-Aviv"
                nb_page (int): Number of google pages we want to scrape to extract profile url
            """
        self.email = email
        self.password = password
        self.driver = webdriver.Chrome()
        # initialize data
        self.url_dic = {}
        self.scraped_page_data = {}
        self.job = job
        self.location = location
        self.nb_pages = nb_pages
        self.sections = sections

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
        query.send_keys(GOOGLE_SEARCH_STRING.format(self.job, self.location))
        query.send_keys(Keys.RETURN)
        sleep(CLICK_WAIT_TIME)

        for i in range(self.nb_pages):

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
                print('Unable to search for any more profiles')
                break

            self.scrape_content_profiles()

    def scrape_content_profiles(self):

        # Get the list of all the LinkedIn profiles
        list_of_urls = self.url_dic.keys()
        print(NUM_PROFILES_FOUND.format(len(list_of_urls)))
        # Loop over all urls to scrape data on it using the class WebPage from scrape_page.py
        for url_profile in list_of_urls:
            try:
                sleep(CLICK_WAIT_TIME)
                this_url = WebPage(url_profile, self.driver, self.sections)
                this_url.get_data()
                self.scraped_page_data.update(this_url.export_data())


            except Exception as ex:
                print(PAGE_SCRAPE_FAILED_ERROR.format(ex, url_profile))
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

    def create_db(self):
        """The function will create the database"""

        if os.path.exists(DB_FILENAME):
            os.remove(DB_FILENAME)

        con = sqlite3.connect(DB_FILENAME)
        cur = con.cursor()

        cur.execute(''' CREATE TABLE `profiles` (
                          `url` varchar(255) PRIMARY KEY,
                          `search_job` varchar(255),
                          `search_location` varchar(255));

                        ''')

        cur.execute(''' CREATE TABLE `institutions` (
                          `id` integer PRIMARY KEY AUTOINCREMENT,
                          `name` varchar(255) UNIQUE

                        );

                        ''')

        cur.execute(''' CREATE TABLE `subjects` (
                          `id` integer PRIMARY KEY AUTOINCREMENT,
                          `name` varchar(255) UNIQUE
                        );

                        ''')

        cur.execute(''' CREATE TABLE `skill_list` (
                          `id` integer PRIMARY KEY AUTOINCREMENT,
                          `name` varchar(255) UNIQUE
                        );

                        ''')

        cur.execute(''' CREATE TABLE `companies` (
                          `id` integer PRIMARY KEY AUTOINCREMENT,
                          `name` varchar(255) UNIQUE
                        );

                        ''')

        cur.execute('''  CREATE TABLE `educations` (
                          `id` integer PRIMARY KEY AUTOINCREMENT,
                          `url` varchar(255),
                          `graduation_type` varchar(255),
                          `id_institution` integer,
                          `id_subject` integer ,
                          `date` datetime,
                          FOREIGN KEY (`url`) REFERENCES `profiles` (`url`),
                          FOREIGN KEY (`id_institution`) REFERENCES `institutions` (`id`),
                          FOREIGN KEY (`id_subject`) REFERENCES `subjects` (`id`)
                        );

                        ''')

        cur.execute(''' CREATE TABLE `skills` (
                          `id` integer PRIMARY KEY AUTOINCREMENT,
                          `url` varchar(255),
                          `id_skill` int,
                          `n_endorsements` int,
                          FOREIGN KEY (`url`) REFERENCES `profiles` (`url`),
                          FOREIGN KEY (`id_skill`) REFERENCES `skill_list` (`id`)
                        );

                        ''')

        cur.execute(''' CREATE TABLE `experiences` (
                          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                          `url` varchar(255),
                          `id_company` integer,
                          `job_name` varchar(255),
                          `start_date` datetime,
                          `duration` datetime,
                          `location` varchar(255),
                          FOREIGN KEY (`url`) REFERENCES `profiles` (`url`),
                          FOREIGN KEY (`id_company`) REFERENCES `companies` (`id`)
                        );

                        ''')
        con.commit()
        self.insert_data(con, cur)

    def insert_data(self, con, cur):
        """The function will insert data inside the database"""

        JOB_SEARCH = self.job
        LOCATION_SEARCH = self.location

        # open the pickle file
        dbfile = open(PICKLE_FILENAME, 'rb')
        db = pickle.load(dbfile)

        """Insert experiments"""
        for url in db.keys():
            for experience in db[url]['Experience']['Data']:

                job_name = 'Nan'
                company_name = 'Nan'
                location = 'Nan'
                duration = 'Nan'
                start_date = 'Nan'

                try:
                    job_name = list(experience.keys())[0]
                except:
                    pass

                try:
                    company_name = experience[job_name]['Company Name']
                except:
                    pass

                try:
                    location = experience[job_name]['Location']
                except:
                    pass

                try:
                    duration = experience[job_name]['Employment Duration']
                except:
                    pass

                try:
                    start_date = experience[job_name]['Dates Employed']

                except:
                    pass

                if job_name in ['Title', 'Company Name']:
                    job_name = 'Nan'

                cur.execute(''' INSERT OR IGNORE INTO companies(name) VALUES(?)''', [company_name])

                cur.execute('''SELECT id FROM companies WHERE name=(?)''', [company_name])

                id_company = cur.fetchone()[0]

                cur.execute(
                    ''' INSERT OR IGNORE INTO experiences(url, id_company, job_name, start_date, duration, location)\
                     VALUES(?,?,?,?,?,?)''',
                    [url, id_company, job_name, start_date, duration, location])

            cur.execute(''' INSERT OR IGNORE INTO profiles(url,search_job,search_location) VALUES(?,?,?)''',
                        [url, JOB_SEARCH, LOCATION_SEARCH])
        con.commit()

        """Education"""
        for url in db.keys():
            for education in db[url]['Education']['Data']:
                institution = 'Nan'
                Degree_Name = 'Nan'
                Field_Of_Study = 'Nan'
                Dates = 'Nan'
                try:
                    institution = list(education.keys())[0]
                except:
                    pass

                try:
                    Degree_Name = education[institution]['Degree Name']
                except:
                    pass

                try:
                    Field_Of_Study = education[institution]['Field Of Study']
                except:
                    pass

                try:
                    Dates = education[institution]['Dates attended or expected graduation']
                except:
                    pass

                cur.execute(''' INSERT OR IGNORE INTO institutions(name) VALUES(?)''', [institution])

                cur.execute('''SELECT id FROM institutions WHERE name=(?)''', [institution])
                id_institution = cur.fetchone()[0]

                cur.execute(''' INSERT OR IGNORE INTO subjects(name) VALUES(?)''', [Field_Of_Study])

                cur.execute('''SELECT id FROM subjects WHERE name=(?)''', [Field_Of_Study])
                id_subject = cur.fetchone()[0]

                cur.execute(
                    ''' INSERT OR IGNORE INTO educations(url, graduation_type, id_institution, id_subject, date ) VALUES(?,?,?,?,?)''', \
                    [url, Degree_Name, id_institution, id_subject, Dates])

        con.commit()

        """Skills"""
        for url in db.keys():
            for skill in db[url]['Skills']['Data']:
                skill_name = 'Nan'
                skill_level = 'Nan'

                try:
                    skill_name = list(skill.keys())[0]
                except:
                    pass

                try:
                    skill_level = skill[skill_name]
                except:
                    pass

                cur.execute(''' INSERT OR IGNORE INTO skill_list(name) VALUES(?)''', [skill_name])

                cur.execute('''SELECT id FROM skill_list WHERE name=(?)''', [skill_name])

                id_skill = cur.fetchone()[0]

                cur.execute(''' INSERT OR IGNORE INTO skills(url,id_skill,n_endorsements) VALUES(?,?,?)''', \
                            [url, id_skill, skill_level])
        con.commit()
        con.close()
