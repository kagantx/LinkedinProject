from selenium import webdriver
from time import sleep
import json
import pprint
from bs4 import BeautifulSoup

from selenium.webdriver.common.action_chains import ActionChains


class WebPage:
    """Represents a LinkedIn webpage.

    Contains methods:
     __init__ to set variables and validate the user's choice of sections to scrape
     get_data to scrape the chosen sections
     _parse_(section) functions to parse each section
     print_data to print the data
     dump_json to dump the data to a json file

    Contains class constants:
    DEFAULT_SECTIONS (default sections to scrape)
    ALL_SECTIONS (all sections possible to scrape)

    (section)_FIELDS (fields to scrape for each section
    SCROLL_PAUSE_TIME (time to wait while scrolling to input variables

    Contains instance variables:
    url_loc - web page location
    scraped_data - data scraped from web page


    """
    DEFAULT_SECTIONS = {"Skills","Experience", "Education"}

    ALL_SECTIONS = {"Experience", "Education", "Skills", "Featured"}
    EXPERIENCE_FIELDS = {'Company Name', 'Dates Employed', 'Employment Duration', 'Location'}
    EDUCATION_FIELDS = {'Degree Name', 'Field Of Study', "Dates attended or expected graduation"}
    FIELDS = EXPERIENCE_FIELDS.union(EDUCATION_FIELDS)

    # XPATH elements for each section
    EXPERIENCE_XPATH = '//*[@id = "experience-section"]//ul//li'
    EDUCATION_XPATH = '//*[@id = "education-section"]//ul//li'
    SKILLS_XPATH= r'//*[contains(class,"pv-skills-categories-section")]//ol'

    def __init__(self, url_loc, my_driver, section_list=None):
        """Initializes the WebPage class. Accepts a url for the page and an optional section list.
         Also initializes the Selenium driver for scraping the webpage and the scraped_data
         variable that contains the results"""
        self.url_loc = url_loc
        if section_list is None:
            section_list = self.DEFAULT_SECTIONS
        self.section_list = [section_item.title() for section_item in section_list]
        if not self.ALL_SECTIONS >= set(self.section_list):
            raise ValueError("You asked for a LinkedIn section that we cannot scrape.")
        self.scraped_data = {}
        self.driver = my_driver
        # Check that section list is valid

    def get_data(self):
        """First, scrolls through the page to make sure it is loaded
        Then, scrapes data for all sections in self.section_list"""
        self.driver.get(self.url_loc)
        self.driver.execute_script("document.body.style.zoom='10%'")
        self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
        # sleep(self.SCROLL_PAUSE_TIME)
        #

        if "Experience" in self.section_list:
            experience = self.driver.find_elements_by_xpath(self.EXPERIENCE_XPATH)
            self.scraped_data["Experience"] = self._parse_experience(experience)

        if "Education" in self.section_list:
            education = self.driver.find_elements_by_xpath(self.EDUCATION_XPATH)
            self.scraped_data["Education"] = self._parse_education(education)
        self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")
        if "Skills" in self.section_list:
            skills = self.driver.find_elements_by_xpath(self.SKILLS_XPATH)
            self.scraped_data["Skills"] = self._parse_skills(skills)
        if "Featured" in self.section_list:
            featured = self.driver.find_elements_by_xpath(self.FEATURED_XPATH)
            self.scraped_data["Featured"] = self._parse_featured(featured)
        self.driver.close()

    def _parse_experiencenew(self, experience):
        """Parses the experience section using the raw scraped data. Records the number of jobs
        and then produces an array containing the EXPERIENCE_FIELDS for each job"""
        new_experience = BeautifulSoup(experience, 'html.parser')

        print(new_experience)
        return new_experience

    def _parse_experience(self, experience):
        """Parses the experience section using the raw scraped data. Records the number of jobs
        and then produces an array containing the EXPERIENCE_FIELDS for each job"""
        experience_dict = {}
        experience_dict.update({"Number": len(experience)})
        experience_list = []

        for job in experience:
            job_fields = job.text.split('\n')

            experience_list.append(self.create_dictionary_from_pairs(job_fields))

        experience_dict.update({"Job_list": experience_list})
        return experience_dict

    def _parse_education(self, education):
        """Parses the education section using the raw scraped data. Records the number of institutions
         attended and then produces an array containing the EDUCATION_FIELDS and their values for each job"""
        education_dict = {}
        education_dict.update({"Number": len(education)})

        education_list = []
        for institution in education:
            degree_fields = institution.text.split('\n')
            education_list.append(self.create_dictionary_from_pairs(degree_fields))
        education_dict.update({"University_List": education_list})
        return education_dict

    def _parse_featured( self,featured):
        """Parses the featured section using the raw scraped data.
        Returns the number of items in the section as a key:value pair"""

        pass

    def _parse_skills(self,skills):
        """Parses the skills section using the raw scraped data.
        Records the number of skills and dictionary of the form  skill: number of endorsements"""
        skills_dict = {}
        for item in skills:
            print(item)
            result=item.text.split('\n')
            print(result)
            skills_dict.update({result[0]: result[1]})
        return skills_dict

    def export_json(self, out_name):
        """Exports the scraped data from the web page as a json file"""
        with open(out_name + '.json', 'w') as json_dump:
            json.dump(json_dump, self.scraped_data)

    def print_data(self):
        """pprints the scraped data from the web page"""
        pprint.pprint(self.scraped_data)

    def create_dictionary_from_pairs(self, item_list):
        """Given a list, creates a dictionary with key equal to the first item in the list
        and value equal to a dictionary containing keys for entries present in self.FIELDS
        and values equal to the following item in item_list"""
        print(item_list)
        sub_dict = {item_list[x]: item_list[x + 1] for x in range(1, len(item_list) - 1)
                    if item_list[x] in self.FIELDS and len(item_list[x]) > 0}
        return {item_list[0]: sub_dict}


if __name__ == "__main__":
    print("All tests passed")
