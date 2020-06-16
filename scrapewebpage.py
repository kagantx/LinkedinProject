from selenium import webdriver
from time import sleep
import json
import pprint

"""my_dict={featured:{num_featured}
experience:{num_jobs:,
            jobs: [{company_name:, position:position,start_date:
                    end_date:}
                   ...]

education:{num_education:x,
            education: [institution_name: {degree_name:degree,start_date:                   }
                   ...]

skills_templagte: {num_skills:x,
        skills:
        {skill_name:n_endorsements,
         }"""


class WebPage:
    """Represents a LinkedIn webpage.

    Contains methods:
     __init__ to set variables and validate the user's choice of sections to scrape
     get_data to scrape the chosen sections
     _parse_(section) functions to parse each section
     print_data() to print the data
     to scrape a LinkedIn profile page and


    """
    DEFAULT_ITEMS = {"Experience", "Education"}

    ALL_ITEMS = {"Experience", "Education", "Skills", "Featured"}
    EXPERIENCE_FIELDS = {'Company Name', 'Dates Employed', 'Employment Duration', 'Location'}
    EDUCATION_FIELDS = {'Degree Name', 'Field Of Study', "Dates attended or expected graduation"}
    FIELDS = EXPERIENCE_FIELDS.union(EDUCATION_FIELDS)

    def __init__(self, url_loc, my_driver, section_list=None):
        """Initializes the WebPage class. Accepts a ur"""
        self.url_loc = url_loc
        if section_list is None:
            section_list = self.DEFAULT_ITEMS
        self.section_list = [section_item.title() for section_item in section_list]
        if not self.ALL_ITEMS >= set(self.section_list):
            raise ValueError("You asked for a LinkedIn section that we cannot scrape.")
        self.scraped_data = {}
        self.driver = my_driver
        # Check that section list is valid

    def get_data(self):
        """First, scrolls through the page to make sure it is loaded
        Then, gets data for all sections unless excluded"""
        self.driver.get(self.url_loc)
        self._scroll_page()

        if "Experience" in self.section_list:
            experience = self.driver.find_elements_by_xpath('//*[@id = "experience-section"]//ul//li')
            self.scraped_data["Experience"] = self._parse_experience(experience)

        if "Education" in self.section_list:
            education = self.driver.find_elements_by_xpath('//*[@id = "education-section"]//ul//li')
            self.scraped_data["Education"] = self._parse_education(education)
        if "Skills" in self.section_list:
            skills = self.driver.find_elements_by_xpath
            self.scraped_data["Skills"] = self._parse_skills(skills)
        if "Featured" in self.section_list:
            featured = self.driver.find_elements_by_xpath
            self.scraped_data["Featured"] = self._parse_featured(featured)

    def _scroll_page(self):
        SCROLL_PAUSE_TIME = 1
        self.driver.execute_script("document.body.style.zoom='10%'")
        self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
        sleep(SCROLL_PAUSE_TIME)
        self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")

    def _parse_experience(self, experience):

        experience_dict = {}
        experience_dict.update({"Number": len(experience)})
        experience_list = []
        for item in experience:
            job_fields = item.text.split('\n')
            print(job_fields)
            experience_list.append(self.create_dictionary_from_pairs(job_fields))

        experience_dict.update({"Job_list": experience_list})
        return experience_dict

    def _parse_education(self, education):
        education_dict = {}
        education_dict.update({"Number": len(education)})

        education_list = []
        for item in education:
            degree_fields = item.text.split('\n')
            education_list.append(self.create_dictionary_from_pairs(degree_fields))
        education_dict.update({"University_List": education_list})
        return education_dict

    def _parse_featured(featured, self):
        pass

    def _parse_skills(skills, self):
        pass

    def export_json(self, out_name):
        with open(out_name + '.json', 'w') as json_dump:
            json.dump(json_dump, self.scraped_data)

    def print_data(self):
        pprint.pprint(self.scraped_data)

    def create_dictionary_from_pairs(self, item_list):
        print(item_list)
        sub_dict = {item_list[x]: item_list[x + 1] for x in range(1, len(item_list) - 1)
                    if item_list[x] in self.FIELDS and len(item_list[x]) > 0}
        return {item_list[0]: sub_dict}


if __name__ == "__main__":
    print("All tests passed")
