import requests
from bs4 import BeautifulSoup
from linkedin_logger import getmylogger
from constants import *
from itertools import chain
import json

logger = getmylogger(__name__)

class UniversityAPI:
    def __init__(self):
        """Initializes the list of API responses"""

        self.university_data = {}

    def get_new_universities(self, linkedin_dict):
        """Takes a list of LinkedIn_scraper scraped profiles and extracts all
        university names. Stores all names not yet queried by the API in the
        self.update_list"""
        self.update_list=[]
        self.success_list=[]

        for scrape in linkedin_dict.values():

            scrape_universities=list({universities for universities in chain(*scrape['Education']['Data'])
                  if universities not in self.university_data})

            self.update_list=self.update_list+scrape_universities
        self.update_list=list(set(self.update_list))

        print(self.update_list)

    def get_data_from_api(self):
        """Queries the API for all universities on self.update_list
        parses the response and returns a list of the API responses, stored as dictionaries"""
        for university in self.update_list:
            try:
                response = requests.get(API_URL.format(university))
                html_soup = BeautifulSoup(response.text, 'html.parser')
                univ_info=json.loads(html_soup.text)
            except Exception as ex:
                logger.error(UNIVERSITY_API_ERROR.format(university, ex))
                continue
            try:
                assert len(univ_info) > 0

            except AssertionError:
                logger.error(NO_DATA_FOR_UNIVERSITY.format(university))
                continue

            try:
                assert set(univ_info[0].keys()) == API_KEYS

            except AssertionError:
                logger.error(BAD_DATA_FOR_UNIVERSITY.format(university))
                continue
            else:
                self.university_data[university]=univ_info[0]
                self.success_list.append(university)




    def return_api_data(self):
        """Returns all successfully queried university data from the current commit"""
        if len(self.success_list)==0:
            logger.warn(NO_DATA_RETURNED)
            return {}
        else:
            return {university:self.university_data[university] for university in self.success_list}

    def extract_api_data(self):
        """Returns all successfully queried university data scraped so far"""
        return self.university_data

if __name__ == "__main__":
    #calling sequence in LinkedinBot
    api=UniversityAPI()
    temp_dict={'a':{
        'Education':{'Data':{'Sorbonne':'hi','Harvard':
                             'bye'}}}}
    api.get_new_universities(temp_dict)
    api.get_data_from_api()
    print(api.extract_api_data())
    print("All tests passed")
