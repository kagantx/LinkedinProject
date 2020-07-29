"""Constants file. Options that are likely to be changed are on top
 At the bottom, a template is given for adding new sections"""

DEFAULT_PICKLE_FILENAME = "profile_pickle"

NUM_SCROLL_POSITIONS = 8

SCROLL_PAUSE_TIME = 0.2
CLICK_WAIT_TIME = 0.5

DEFAULT_JOB = 'Data Scientist'
DEFAULT_LOCATION = 'Tel Aviv'
DEFAULT_PAGES_TO_SCRAPE = 1

# API constants
API_URL = "http://universities.hipolabs.com/search?name={}"

API_KEYS = {'name', 'state-province', 'country', 'domains', 'alpha_two_code', 'web_pages'}

NO_DATA_RETURNED = "Did not successfull get any University data from the API"

BAD_DATA_FOR_UNIVERSITY = "Found invalid data for university {}"

NO_DATA_FOR_UNIVERSITY = "Found no data for university {}"

UNIVERSITY_API_ERROR = "Unable to reach API for university data for university {}. Got Exception {}"

PAGE_DATA_ADDED_DB = "Added data to database for url {}"

FAILED_SECTION_INSERT = "Failed to add part of profile to database: got error: {}"

API_GOT_ERROR = "Got error when scraping API data; got error: {}"
# constants for setting fields in scrape_page.py
EXPERIENCE_FIELDS = {'Company Name', 'Dates Employed', 'Employment Duration', 'Location'}
EDUCATION_FIELDS = {'Degree Name', 'Field Of Study', "Dates attended or expected graduation"}
FIELDS = EXPERIENCE_FIELDS.union(EDUCATION_FIELDS)

DICTIONARY_SECTIONS = {"Experience", "Education"}
SKIP_ONE_SECTIONS = {"Skills"}

# constants for finding sections in scrape_page.py
LOCS = {}
XPATHS = {}

# XPATH locations for each section (loc) and its fields (xpath)
LOCS["Experience"] = '//*[@id = "experience-section"]'
LOCS["Education"] = '//*[@id = "education-section"]'
LOCS["Skills"] = '//*[@class="pv-profile-section pv-skill-categories-section artdeco-container-card ember-view"]'

XPATHS["Experience"] = ''.join([LOCS["Experience"], r"//ul//li"])
XPATHS["Education"] = ''.join([LOCS["Education"], r"//ul//li"])
XPATHS["Skills"] = ''.join([LOCS["Skills"], r"//li"])

FAILED_SECTION_SCRAPE = "Failed to parse section: {}.\n Got Error: {}"

SCROLL_COMMAND = "window.scrollTo(0, document.body.scrollHeight*{});"

# Constants for login in linkedin_base

ASK_LOGIN_XPATH = '/html/body/nav/a[3]'
USER_NAME_XPATH = '//*[@id="username"]'
PASSWORD_XPATH = '//*[@id="password"]'
LOGIN_BUTTON_XPATH = '//*[@id="app__container"]/main/div[2]/form/div[3]/button'
PAGE_SCRAPE_FAILED_ERROR = "Completely failed to scrape profile {}. Got exception {}"

# Constants for searching in linkedin_base
GOOGLE_URL = 'https://www.google.com/'
GOOGLE_SEARCH_BAR_XPATH = '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
GOOGLE_NEXT_PAGE = '//*[@id="pnnext"]/span[2]'

LINKEDIN_PREFIX = "https://www.linkedin.com/in/"
GOOGLE_SEARCH_STRING = "site:linkedin.com/in/ AND {} AND {}"
NUM_PROFILES_FOUND = "Found {} profiles to scrape"
NUM_NEW_PROFILES_FOUND = "Found {} new profiles to scrape"
CORRECT_GOOGLE_RESULT_ID = 'eipWBe'
LINKEDIN_MAIN_URL = 'https://www.linkedin.com/'

PROFILE_SCRAPING_MESSAGE = 'Scraping profile at url {}'
URL_START_INDEX = 2
URL_END_INDEX = -3

SEARCHED_GOOGLE = "Searched google for your search terms {} and {}"
NO_MORE_PROFILES_MESSAGE = 'Unable to search for any more profiles'
SUCCESSFULLY_LOGGED_IN = "Successfully logged in"
SUCCESSFUL_SCRAPES_DONE = "Successfully scraped {} profiles"
# Constants on top level linkedin_scraper

NO_PAGES_REQUESTED = "You must ask to scrape at least one page"
INVALID_SECTION_REQUESTED = "You asked us to scrape a section we cannot scrape. Your input was: {}"
SECTION_DICT = {'x': "Experience", 'e': 'Education', 's': 'Skills'}
SECTIONS_LOC = ["E(x)perience", "(E)ducation", "(S)kills"]
SECTION_LETTERS_DEFAULT = 'xes'
SECTIONS_HELP = f"""Sections to scrape. Please use single letters for 
                {SECTIONS_LOC[0]}, {SECTIONS_LOC[1]}, {SECTIONS_LOC[2]} 
                    without spaces in any order"""

# Constants for database module

REMOVED_DATABASE_SUCCESS = "Removed the database : {} successfully"

NO_DATABASE_TO_REMOVE = "Didn't find a database to remove: {}"

DATABASE_EXISTS = "The database {} already exists. Opening ..."

OPENED_DATABASE_FILE = "Opened database file"

DATABASE_CREATION_SUCCESS = "Created database {} successfully"

# SQL Queries

CREATE_DB_IF_NOT_EXIST = "CREATE DATABASE IF NOT EXISTS linkedin"
USE_DB = "USE linkedin"
CREATE_EXPERIENCES_TABLE = ''' CREATE TABLE `experiences` (
                          `id` INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          `url` varchar(255),
                          `id_company` integer,
                          `job_name` varchar(255),
                          `start_date` datetime,
                          `duration` datetime,
                          `location` varchar(255),
                          FOREIGN KEY (`url`) REFERENCES `profiles` (`url`),
                          FOREIGN KEY (`id_company`) REFERENCES `companies` (`id`)
                        );

                        '''

CREATE_SKILLS_TABLE = ''' CREATE TABLE `skills` (
                          `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          `url` varchar(255),
                          `id_skill` int,
                          `n_endorsements` int,
                          FOREIGN KEY (`url`) REFERENCES `profiles` (`url`),
                          FOREIGN KEY (`id_skill`) REFERENCES `skill_list` (`id`)
                        );

                        '''

CREATE_EDUCATIONS_TABLE = '''  CREATE TABLE `educations` (
                          `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          `url` varchar(255),
                          `graduation_type` varchar(255),
                          `id_institution` integer,
                          `id_subject` integer ,
                          `date` datetime,
                          FOREIGN KEY (`url`) REFERENCES `profiles` (`url`),
                          FOREIGN KEY (`id_institution`) REFERENCES `institutions` (`id`),
                          FOREIGN KEY (`id_subject`) REFERENCES `subjects` (`id`)
                        );

                        '''

CREATE_COMPANIES_TABLE = ''' CREATE TABLE `companies` (
                          `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          `name` varchar(255) UNIQUE
                        );

                        '''

CREATE_SKILL_LIST_TABLE = ''' CREATE TABLE `skill_list` (
                          `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          `name` varchar(255) UNIQUE
                        );

                        '''

CREATE_SUBJECTS_TABLE = ''' CREATE TABLE `subjects` (
                          `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          `name` varchar(255) UNIQUE
                        );

                        '''

CREATE_INSTITUTION_TABLE = ''' CREATE TABLE `institutions` (
                          `id` integer PRIMARY KEY NOT NULL AUTO_INCREMENT,
                          `name` varchar(255) UNIQUE,
                          `formal_name` varchar(255), 
                          `country` varchar(255),
                          `web_page` varchar(255),
                          `domain` varchar(255),
                          `country_code` varchar(2)
                        );

                        '''

CREATE_PROFILES_TABLE = ''' CREATE TABLE `profiles` (
                          `url` varchar(255) PRIMARY KEY,
                          `search_job` varchar(255),
                          `search_location` varchar(255));

                        '''

CREATE_TABLE_LIST = [CREATE_PROFILES_TABLE, CREATE_INSTITUTION_TABLE, CREATE_SUBJECTS_TABLE,
                     CREATE_SKILL_LIST_TABLE, CREATE_COMPANIES_TABLE, CREATE_EDUCATIONS_TABLE, CREATE_SKILLS_TABLE,
                     CREATE_EXPERIENCES_TABLE]

SELECT_OLD_URLS = '''SELECT url FROM profiles'''

INSERT_COMPANIES_NAME = ''' INSERT  IGNORE INTO companies(name) VALUES(%s)'''
SELECT_ID_COMPANY = '''SELECT id FROM companies WHERE name=%s'''
INSERT_EXPERIENCES = ''' INSERT  IGNORE INTO experiences(url, id_company, job_name, start_date, duration, location)\
                     VALUES(%s,%s,%s,%s,%s,%s)'''
INSERT_PROFILES = ''' INSERT  IGNORE INTO profiles(url,search_job,search_location) VALUES(%s,%s,%s)'''
INSERT_INSTITUTIONS = """ INSERT  IGNORE INTO institutions(name,formal_name,country, web_page,
                        domain,country_code) VALUES(%s,%s,%s,%s,%s,%s) """
INSERT_INSTITUTIONS_NAME = ''' INSERT  IGNORE INTO institutions(name) VALUES(%s)'''
SELECT_ID_INSTITUTIONS = '''SELECT id FROM institutions WHERE name=%s'''
INSERT_SUBJECTS = ''' INSERT  IGNORE INTO subjects(name) VALUES(%s)'''
SELECT_ID_SUBJECTS = '''SELECT id FROM subjects WHERE name=%s'''
INSERT_EDUCATIONS = """ INSERT  IGNORE INTO educations(url, graduation_type, id_institution, id_subject, date ) 
                            VALUES(%s,%s,%s,%s,%s)"""
INSERT_SKILLS_NAME = ''' INSERT  IGNORE INTO skill_list(name) VALUES(%s)'''
SELECT_ID_SKILLS = '''SELECT id FROM skill_list WHERE name=%s'''
INSERT_SKILLS = ''' INSERT  IGNORE INTO skills(url,id_skill,n_endorsements) VALUES(%s,%s,%s)'''

# SQL field names

EXPERIENCE = 'Experience'
DATA = 'Data'
COMPANY_NAME = 'Company Name'
LOCATION = 'Location'
EMPLOYMENT_DURATION = 'Employment Duration'
DATES_EMPLOYED = 'Dates Employed'
TITLE = 'Title'
EDUCATION = 'Education'
DEGREE_NAME = 'Degree Name'
FIELD_OF_STUDY = 'Field Of Study'
DATES_ATTENDED = 'Dates attended or expected graduation'
NAME = 'name'
ALPHA_CODE = 'alpha_two_code'
DOMAINS = 'domains'
COUNTRY = 'country'
WEB_PAGES = 'web_pages'
SKILLS = 'Skills'
# Template for adding sections
#
# FOO_FIELDS = {foo_field1, ...}
# FIELDS = FIELDS.union(FOO_FIELDS)
# SECTION_DICT.update({foo_first_letter:foo_name})
# LOCS.update({foo_name: foo_loc})
# XPATHS.update({foo_name:foo_loc+foo_xpath_extra})
# add to SKIP_ONE_SECTIONS or DICTIONARY_SECTIONS if it has the same
# format as one of them. Otherwise, need to modify scrape_page.py


# database

DEFAULT_DB_FILENAME = 'linkedin'

if __name__ == "__main__":
    print("All tests passed")
