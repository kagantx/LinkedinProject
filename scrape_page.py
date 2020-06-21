from time import sleep
import json
import pprint

from selenium.webdriver.common.action_chains import ActionChains


class WebPage:
    """Represents a LinkedIn webpage.

    Contains methods:
     __init__ to set variables and validate the user's choice of sections to scrape

     _get_data to scrape the chosen sections
     _parse_data to parse each section
     _scroll_page  to ensure the web page is loaded

     print_data to print the data
     dump_json to dump the data to a json file
     export_data to export the data to another program

    Contains class constants:
    DEFAULT_SECTIONS (default sections to scrape)
    ALL_SECTIONS (all sections possible to scrape)
    XPATHS and LOCS (Xpath and location for each section)
    (section)_FIELDS (fields to scrape for each section
    SCROLL_PAUSE_TIME (time to wait while scrolling to input variables

    Contains instance variables:
    url - web page location
    scraped_data - data scraped from web page

    """
    DEFAULT_SECTIONS = ["Skills", "Experience", "Education"]

    ALL_SECTIONS = {"Experience", "Education", "Skills"}
    EXPERIENCE_FIELDS = {'Company Name', 'Dates Employed', 'Employment Duration', 'Location'}
    EDUCATION_FIELDS = {'Degree Name', 'Field Of Study', "Dates attended or expected graduation"}
    FIELDS = EXPERIENCE_FIELDS.union(EDUCATION_FIELDS)

    LOCS = {}
    XPATHS = {}
    # XPATH locations for each section (loc) and its fields (xpath)
    LOCS["Experience"] = '//*[@id = "experience-section"]'
    LOCS["Education"] = '//*[@id = "education-section"]'
    LOCS["Skills"] = '//ol'
    # Alternative skills LOC:
    # '[@class="pv-skill-categories-section__top-skills pv-profile-section__section-info section-info pb1")]'
    # Neither works all the time

    XPATHS["Experience"] = ''.join([LOCS["Experience"], r"//ul//li"])
    XPATHS["Education"] = ''.join([LOCS["Education"], r"//ul//li"])
    XPATHS["Skills"] = ''.join([LOCS["Skills"], r"//li"])

    SCROLL_PAUSE_TIME = 1

    def __init__(self, url, my_driver, section_list=None, output_file="web_page"):
        """Initializes the WebPage class. Accepts a url for the page and an optional section list.
         Also initializes the Selenium driver for scraping the webpage and the scraped_data
         variable that contains the results"""
        self.url = url
        if section_list is None:
            section_list = self.DEFAULT_SECTIONS
        self.section_list = [section_item.title() for section_item in section_list]
        if not self.ALL_SECTIONS >= set(self.section_list):
            raise ValueError("You asked for a LinkedIn section that we cannot scrape.")
        self.output_file = output_file

        # Initialize data to
        self.scraped_data = {}
        self.scraped_data[self.url] = {}
        self.driver = my_driver

    def get_data(self):
        """Goes to the url of the chosen page.
        Scrolls through the page to make sure it is loaded
        Then, scrapes data for all sections in self.section_list"""

        self.driver.get(self.url)

        self._scroll_page()

        for section in self.section_list:
            try:
                section_data = self._get_section(section)
            except Exception as ex:
                print("Failed to parse section: {}.\n Got Error: {}".format(section, ex))
                self.scraped_data[self.url].update({section: {}})
            else:
                self.scraped_data[self.url].update({section: section_data})

    def _scroll_page(self):
        """Scrolls through the web page to ensure that all elements of the page can be loaded"""
        self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/4));")
        sleep(self.SCROLL_PAUSE_TIME)
        self.driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
        sleep(self.SCROLL_PAUSE_TIME)
        self.driver.execute_script("window.scrollTo(0, (3*document.body.scrollHeight/4));")

    def _get_section(self, section):
        """Gets the data for a section. First, it scrolls to the section on the web page
        Then it gets the data using the XPATH of the section. Finally, it parses the data."""
        ActionChains(self.driver).move_to_element(
            self.driver.find_element_by_xpath(self.LOCS[section])).perform()
        section_data = self.driver.find_elements_by_xpath(self.XPATHS[section])
        return self._parse_data(section, section_data)

    def _parse_data(self, section, data):
        """Parses the data.
        The education and experience sections have field:value pairs
        which we parse for each valid field as defined at the beginning of the class using
        the function create_dictionary_from_pairs.
        The skills section always has valid fields skill_name and n_endorsements, so we
        don't need to filter it"""
        output_dictionary = {}
        inner_list = []
        output_dictionary.update({"Number of Entries": len(data)})

        for entry in data:
            entry_fields = entry.text.split('\n')
            if section in ["Experience", "Education"]:
                inner_list.append(self.create_dictionary_from_pairs(entry_fields))
            if section in ["Skills"]:
                if len(entry_fields) > 1:
                    inner_list.append({entry_fields[0]: entry_fields[2]})
                else:
                    inner_list.append({entry_fields[0]: '0'})
        output_dictionary.update({"Data": inner_list})
        return output_dictionary

    def create_dictionary_from_pairs(self, item_list):
        """Given a list, creates a dictionary with key equal to the first item in the list
        and value equal to a dictionary containing keys for entries present in self.FIELDS
        and values equal to the following item in item_list"""
        sub_dict = {item_list[x]: item_list[x + 1] for x in range(1, len(item_list) - 1)
                    if item_list[x] in self.FIELDS and len(item_list[x]) > 0}
        return {item_list[0]: sub_dict}

    def export_json(self, out_name):
        """Exports the scraped data from the web page as a json file"""
        with open(out_name + '.json', 'w') as json_dump:
            json.dump(self.scraped_data, json_dump)

    def print_data(self):
        """pprints the scraped data from the web page"""
        pprint.pprint(self.scraped_data)

    def export_data(self):
        """Exports the data as a dictionary"""
        return self.scraped_data


if __name__ == "__main__":
    print("All tests passed")