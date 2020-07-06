"""Constants file. Options that are likely to be changed are on top
 At the bottom, a template is given for adding new sections"""

PICKLE_FILENAME='profile_pickle'
NUM_SCROLL_POSITIONS=8

SCROLL_PAUSE_TIME = 0.5
CLICK_WAIT_TIME=1

DEFAULT_JOB='Data Scientist'
DEFAULT_LOCATION='Tel Aviv'
DEFAULT_PAGES_TO_SCRAPE=1

#constants for setting fields in scrape_page.py
EXPERIENCE_FIELDS = {'Company Name', 'Dates Employed', 'Employment Duration', 'Location'}
EDUCATION_FIELDS = {'Degree Name', 'Field Of Study', "Dates attended or expected graduation"}
FIELDS = EXPERIENCE_FIELDS.union(EDUCATION_FIELDS)

DICTIONARY_SECTIONS={"Experience", "Education"}
SKIP_ONE_SECTIONS={"Skills"}

#constants for finding sections in scrape_page.py
LOCS = {}
XPATHS = {}

# XPATH locations for each section (loc) and its fields (xpath)
LOCS["Experience"] = '//*[@id = "experience-section"]'
LOCS["Education"] = '//*[@id = "education-section"]'
LOCS["Skills"] = '//*[@class="pv-profile-section pv-skill-categories-section artdeco-container-card ember-view"]'

XPATHS["Experience"] = ''.join([LOCS["Experience"], r"//ul//li"])
XPATHS["Education"] = ''.join([LOCS["Education"], r"//ul//li"])
XPATHS["Skills"] = ''.join([LOCS["Skills"], r"//li"])

FAILED_SECTION_SCRAPE_MESSAGE="Failed to parse section: {}.\n Got Error: {}"

SCROLL_COMMAND="window.scrollTo(0, document.body.scrollHeight*{});"

#Constants for login in linkedin_base

ASK_LOGIN_XPATH='/html/body/nav/a[3]'
USER_NAME_XPATH='//*[@id="username"]'
PASSWORD_XPATH='//*[@id="password"]'
LOGIN_BUTTON_XPATH='//*[@id="app__container"]/main/div[2]/form/div[3]/button'
PAGE_SCRAPE_FAILED_ERROR="Completely failed to scrape profile {}. Got exception {}"

#Constants for searching in linkedin_base
GOOGLE_URL = 'https://www.google.com/'
GOOGLE_SEARCH_BAR_XPATH = '//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input'
GOOGLE_NEXT_PAGE = '//*[@id="pnnext"]/span[2]'

LINKEDIN_PREFIX = "https://www.linkedin.com/in/"
GOOGLE_SEARCH_STRING="site:linkedin.com/in/ AND {} AND {}"
NUM_PROFILES_FOUND="Found {} profiles to scrape"
CORRECT_GOOGLE_RESULT_ID='eipWBe'
LINKEDIN_MAIN_URL='https://www.linkedin.com/'
URL_START_INDEX=2
URL_END_INDEX=-3

NO_MORE_PROFILES_MESSAGE='Unable to search for any more profiles'

#Constants on top level linkedin_scraper

NO_PAGES_REQUESTED="You must ask to scrape at least one page"
INVALID_SECTION_REQUESTED="You asked us to scrape a section we cannot scrape. Your input was: {}"
SECTION_DICT={'x':"Experience",'e':'Education','s':'Skills'}

# Template for adding sections
#
# FOO_FIELDS = {foo_field1, ...}
# FIELDS = FIELDS.union(FOO_FIELDS)
# SECTION_DICT.update({foo_first_letter:foo_name})
# LOCS.update({foo_name: foo_loc})
# XPATHS.update({foo_name:foo_loc+foo_xpath_extra})
# add to SKIP_ONE_SECTIONS or DICTIONARY_SECTIONS if it has the same
#format as one of them. Otherwise, need to modify scrape_page.py



if __name__=="__main__":


    print("All tests passed")