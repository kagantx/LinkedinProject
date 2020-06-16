from selenium import webdriver
from time import sleep
import json
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
    DEFAULT_ITEMS = ["Experience", "Education", "Skills"]
    ALL_ITEMS= ["Experience", "Education", "Skills", "Featured"]

    def __init__(self, url_loc, select_sections=False, section_list=None):
        self.url_loc = url_loc
        self.select_sections = select_sections
        self.section_list = None
        if section_list is not None:
            self.section_list = [section_item.title() for section_item in section_list]
        self.scraped_data = {}
        self.driver=webdriver.Chrome()
        #Check that section list is valid
        self.check_sections()

    def _check_sections(self):
        if self.select_sections:
            for profile_section in self.selection_list:
                if profile_section.title() not in ALL_ITEMS:
                    raise ValueError("You asked for a LinkedIn section that we cannot scrape.")

        else:
            self.selection_list = DEFAULT_ITEMS

    def get_data(self):
        """First, scrolls through the page to make sure it is loaded
        Then, gets data for all sections unless excluded"""

        self._scroll_page()

        if "Experience" in self.selection_list:
            experience_data = self._get_experience()
            self.scraped_data["Experience"] = experience_data
        if "Education" in self.selection_list:
            education_data = self._get_education()
            self.scraped_data["Education"] = education_data
        if "Skills" not in self.selection_list:
            skills_data = self._get_experience()
            self.scraped_data["Skills"] = skills_data
        if "Featured" in self.selection_list:
            experience_data = self._get_featured()
            self.scraped_data["Featured"] = featured_data

    def _scroll_page(self):
        SCROLL_PAUSE_TIME = 1
        self.driver.execute_script("document.body.style.zoom='10%'")
        self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
        sleep(SCROLL_PAUSE_TIME)
        self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")

    def _get_experience(self):
        experience = self.driver.find_elements_by_xpath('//*[@id = "experience-section"]//ul//li')

    def _get_education(self):
        education = self.driver.find_elements_by_xpath('//*[@id = "education-section"]//ul//li')

    def _get_featured(self):
        features =

    def _get_skills(self):



    def export_data_json(self, out_name):
        with open(out_name + '.json', 'w') as json_dump:
            json.dump(json_dump, self.scraped_data)


if __name__ == "__main__":
    print("All tests passed")
