import requests
from bs4 import BeautifulSoup
from linkedin_logger import getmylogger
from constants import *
from itertools import chain
import json

logger = getmylogger(__name__)


class UniversityAPI:
    """
    Represents an API that is queried for data on universities/institutions
    Has methods:
        get_new_universities to find new educational institutions from Linkedin
        get_data_from_api to find data on each new institution
        clean_data to get universities into proper format for queries
        remove_the,remove_of to get rid of possibly problematic words
        return_api_data to return current universities with successful API data
        extract_api_data to return all universities with successful API data
    """

    def __init__(self):
        """Initializes the list of API responses"""

        self.university_data = {}

    def get_new_universities(self, linkedin_dict):
        """Takes a list of LinkedIn_scraper scraped profiles and extracts all
        university names. Stores all names not yet queried by the API in the
        self.update_list"""
        self.update_list = []
        self.success_list = []

        for scrape in linkedin_dict.values():
            scrape_universities = list({universities for universities in chain(*scrape['Education']['Data'])
                                        if universities not in self.university_data})

            self.update_list = self.update_list + scrape_universities
        self.update_list = list(set(self.update_list))

    def get_data_from_api(self):
        """Queries the API for all universities on self.update_list
        parses the response and returns a list of the API responses, stored as dictionaries"""
        for university in self.update_list:
            try:
                univ_info = []
                # try all unique combinations
                univ_clean = self.clean_string(university)
                university_parses = list({university, univ_clean, self.remove_the(univ_clean),
                                          self.remove_of(univ_clean)})
                for query in university_parses:
                    response = requests.get(API_URL.format(query))
                    html_soup = BeautifulSoup(response.text, 'html.parser')
                    univ_info += json.loads(html_soup.text)

            except Exception as ex:
                logger.debug(UNIVERSITY_API_ERROR.format(university, ex))
                continue
            try:
                assert len(univ_info) > 0

            except AssertionError:
                logger.debug(NO_DATA_FOR_UNIVERSITY.format(university))
                continue

            try:
                assert set(univ_info[0].keys()) == API_KEYS

            except AssertionError:
                logger.debug(BAD_DATA_FOR_UNIVERSITY.format(university))
                continue
            else:
                self.university_data[university] = univ_info[0]
                self.success_list.append(university)

    def extract_api_data(self):
        """Returns all successfully queried university data scraped so far"""
        return self.university_data

    def return_api_data(self):
        """Returns all successfully queried university data from the current commit"""
        if len(self.success_list) == 0:
            logger.debug(NO_DATA_RETURNED)
            return {}
        else:
            return {university: self.university_data[university] for university in self.success_list}

    def clean_string(self, string):
        """Format university name so that it has proper capitalization.
        the and of are capitalized only at the start of the university name"""
        string = string.title()
        string = string.strip()
        string = string.replace(' The ', ' the ')
        string = string.replace(' Of ', ' of ')
        string = string.replace(',', '')
        string = string.strip()
        return string

    def remove_the(self, string):
        """Remove the from the string. Assumes clean_string has already been called"""
        string = string.replace('The ', '')
        string = string.replace(' the ', '')
        string = string.strip()
        return string

    def remove_of(self, string):
        """Remove of from the string. Assumes clean_string has already been called"""
        string = string.replace('Of ', '')
        string = string.replace(' of ', '')
        string = string.strip()
        return string


if __name__ == "__main__":
    # calling sequence in LinkedinBot
    api = UniversityAPI()
    temp_dict = {'a': {
        'Education': {'Data': [{'Sorbonne': 'hi'}, {'Harvard':
                                                        'bye'}]}}}
    api.get_new_universities(temp_dict)
    api.get_data_from_api()
    print(api.extract_api_data())
    print("All tests passed")
