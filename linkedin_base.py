from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from scrape_page import WebPage
import pickle


class LinkedinBot:
    """Represents a LinkedIn url profile scraper bot.

        Contains methods:
            __init__ to set variables and validate the user's choice of job and location to scrape
            login function to connect on Linkedin web site
            scrap_url_profile function to scrape every valid url profile
            save_result function to dump the scrape data to a pickle file
            load_result function to load the scrape data to a pickle file

        Contains class constants:
            PREFIX ="https://www.linkedin.com/in/"
     """

    PREFIX = "https://www.linkedin.com/in/"

    def __init__(self, email,password,job="data scientist", location="Tel Aviv", nb_pages=2):

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

    def login(self):
        """ This function logs in to the LinkedIn web site"""
        self.driver.get('https://www.linkedin.com/')

        # Ask LinkedIn to let us log in
        login_btn_1 = self.driver.find_element_by_xpath('/html/body/nav/a[3]')
        login_btn_1.click()

        sleep(1)

        # Enter email address as username
        email_in = self.driver.find_element_by_xpath('//*[@id="username"]')
        email_in.send_keys(self.email)

        # enter the password
        pw_in = self.driver.find_element_by_xpath('//*[@id="password"]')
        pw_in.send_keys(self.password)

        # log in to the website
        login_btn_2 = self.driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button')
        login_btn_2.click()

    def scrape_url_profiles(self):
        """ This function searches google for profiles on LinkedIn
        that match the search terms given by the user"""
        self.driver.get('https://www.google.com/')

        # the search bar to input query
        query = self.driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')

        # Seach google for our search terms in the google browser
        query.send_keys(f'site:linkedin.com/in/ AND "{self.job}" AND "{self.location}"')
        query.send_keys(Keys.RETURN)
        sleep(1)

        for i in range(self.nb_pages):

            # Find links that correspond to search results
            linkedin_urls = self.driver.find_elements_by_class_name('eipWBe')

            # Find valid urls by ensuring they do not contain '...' and have length > 0
            # If they are not already in the url_dic, save them in url_dic
            for url in linkedin_urls:

                if len(url.text) != 0 and url.text[-3:] != '...':
                    cur_url=self.PREFIX + url.text[2:] + '/'
                    if cur_url not in self.url_dic:
                        self.url_dic[cur_url] = 1

            # Try to click on next google page to scrape new profile until it becomes impossible
            try:
                next_btn = self.driver.find_element_by_xpath('//*[@id="pnnext"]/span[2]')
                next_btn.click()
                sleep(2)

            except:
                print('Unable to search for any more profiles')
                break

        # Get the list of all the LinkedIn profiles
        list_of_urls = self.url_dic.keys()
        print("Found {} profiles to scrape".format(len(list_of_urls)))
        # Loop over all urls to scrape data on it using the class WebPage from scrape_page.py
        for url_profile in list_of_urls:
            try:
                sleep(1)
                this_url = WebPage(url_profile, self.driver)
                this_url.get_data()
                self.scraped_page_data.update(this_url.export_data())


            except Exception as ex:
                print("Got Exception {} while trying to scrape profile {}".format(ex,url_profile))
                print("Moving on to next profile")
                continue

        self.driver.close()

    def save_result(self):
        """The function saves our result in a pickle file"""

        dbfile = open('profile_pickle', 'wb')
        pickle.dump(self.scraped_page_data, dbfile)
        dbfile.close()

    def load_result(self):
        """The function loads our result from the pickle file"""

        dbfile = open('profile_pickle', 'rb')
        db = pickle.load(dbfile)
        print(db)
        dbfile.close()


if __name__ == '__main__':
    bot = LinkedinBot(nb_pages=10)
    bot.login()
    bot.scrape_url_profiles()
    bot.save_result()
    bot.load_result()
