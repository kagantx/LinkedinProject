import selenium
"Section"

my_dict={featured:{num_featured}
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
         }
class WebPage:
    def __init__(self,url_loc,exclusion_list=None):
        self.url_loc=url_loc
        self.exclusion_list=exclusion_list
        self.scraped_data={}
    def get_data(self):
        """First, scrolls through the page to make sure it is loaded
        Then, gets data for all sections unless excluded"""

        self._scroll_page()
        if "experience" not in self.exclusion_list:
            experience_data=self._get_experience()
            self.scraped_data["experience"]=experience_data
        if "education" not in self.exclusion_list:
            experience_data = self._get_experience()
            self.scraped_data["experience"] = experience_data
        self._get_featured()

    def _scroll_page(self):
        SCROLL_PAUSE_TIME = 1
        driver.execute_script("document.body.style.zoom='10%'")
        driver.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
        sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, (document.body.scrollHeight));")

    def _get_experience(self,experience_template):
        experience = driver.find_elements_by_xpath('//*[@id = "experience-section"]//ul//li')


    def _get_education(self,education_template):
        education = driver.find_elements_by_xpath('//*[@id = "education-section"]//ul//li')

    def _get_featured(self,featured_template):

    def _web_data.get_skills(skills_template):
def export_data(result_dict, out_name):
    with open(out_name+'.json', 'w') as json_dump:
        json.dump(json_dump, fp)










if __name__=="__main__":



    print("All tests passed")