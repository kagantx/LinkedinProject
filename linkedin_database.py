from constants import *
import os
import sqlite3
import pickle
from linkedin_logger import getmylogger

logger = getmylogger(__name__)


class LinkedinDatabase:
    """
    Represents a database to store Linkedin and api data
    Contains methods:
        create_db to create a new database or open the current one
        remove_db to remove the database file if the user wants a new database
        insert_experience,insert_educations,insert_skills to add data to the database
        close to close the database
        The database structure is in data_design.pdf

    """

    def __init__(self, job=DEFAULT_JOB, location=DEFAULT_LOCATION, database_file=DEFAULT_DB_FILENAME):
        self.job = job
        self.location = location
        self.database_file = database_file
        self.old_urls = []

    def create_db(self):
        """The function will create the database or open it"""
        if not os.path.exists(self.database_file):
            self.con = sqlite3.connect(self.database_file)
            self.cur = self.con.cursor()
            for table_statement in CREATE_TABLE_LIST:
                self.cur.execute(table_statement)

            self.con.commit()
            logger.info(DATABASE_CREATION_SUCCESS.format(self.database_file))

        else:
            logger.info(DATABASE_EXISTS.format(self.database_file))
            self.con = sqlite3.connect(self.database_file)
            self.cur = self.con.cursor()
            # Get list of urls that are already in the database
            self.cur.execute(SELECT_OLD_URLS)
            old_url_response = self.cur.fetchall()
            self.old_urls = [value[0] for value in old_url_response]
            logger.info(OPENED_DATABASE_FILE)

    def remove_db(self):
        try:
            os.remove(self.database_file)
            logger.info(REMOVED_DATABASE_SUCCESS.format(self.database_file))

        except Exception as ex:
            logger.info(NO_DATABASE_TO_REMOVE.format(self.database_file))

    def insert_experience(self, dic_scrap_profile):
        """Inserts data into profiles,companies, and experience tables"""
        for url in dic_scrap_profile:
            self.cur.execute(INSERT_PROFILES, [url, self.job, self.location])

            for experience in dic_scrap_profile[url][EXPERIENCE][DATA]:

                job_name = 'Nan'
                company_name = 'Nan'
                location = 'Nan'
                duration = 'Nan'
                start_date = 'Nan'

                try:
                    job_name = list(experience.keys())[0]
                except:
                    pass

                try:
                    company_name = experience[job_name][COMPANY_NAME]
                except:
                    pass

                try:
                    location = experience[job_name][LOCATION]
                except:
                    pass

                try:
                    duration = experience[job_name][EMPLOYMENT_DURATION]
                except:
                    pass

                try:
                    start_date = experience[job_name][DATES_EMPLOYED]

                except:
                    pass

                if job_name in [TITLE, COMPANY_NAME]:
                    job_name = 'Nan'

                self.cur.execute(INSERT_COMPANIES_NAME, [company_name])

                self.cur.execute(SELECT_ID_COMPANY, [company_name])

                id_company = self.cur.fetchone()[0]

                self.cur.execute(INSERT_EXPERIENCES, [url, id_company, job_name, start_date, duration, location])

        self.con.commit()

    def insert_education(self, dic_scrap_profile, api_result):

        """Inserts institutions, subjects, and educations and also inserts
        data from the API"""

        for url in dic_scrap_profile:
            for education in dic_scrap_profile[url][EDUCATION][DATA]:
                institution = 'Nan'
                Degree_Name = 'Nan'
                Field_Of_Study = 'Nan'
                Dates = 'Nan'
                try:
                    institution = list(education.keys())[0]
                except:
                    pass

                try:
                    Degree_Name = education[institution][DEGREE_NAME]
                except:
                    pass

                try:
                    Field_Of_Study = education[institution][FIELD_OF_STUDY]
                except:
                    pass

                try:
                    Dates = education[institution][DATES_ATTENDED]
                except:
                    pass
                if institution in api_result:
                    formal_name = api_result[institution][NAME]
                    alpha_code = api_result[institution][ALPHA_CODE]
                    domain = api_result[institution][DOMAINS][0]
                    country = api_result[institution][COUNTRY]
                    web_page = api_result[institution][WEB_PAGES][0]
                    self.cur.execute(INSERT_INSTITUTIONS,
                                     [institution, formal_name, country, web_page, domain, alpha_code])
                else:
                    self.cur.execute(INSERT_INSTITUTIONS_NAME, [institution])

                self.cur.execute(SELECT_ID_INSTITUTIONS, [institution])
                id_institution = self.cur.fetchone()[0]

                self.cur.execute(INSERT_SUBJECTS, [Field_Of_Study])

                self.cur.execute(SELECT_ID_SUBJECTS, [Field_Of_Study])
                id_subject = self.cur.fetchone()[0]

                self.cur.execute(INSERT_EDUCATIONS, [url, Degree_Name, id_institution, id_subject, Dates])

        self.con.commit()

    def insert_skills(self, dic_scrap_profile):
        """Inserts data into the skills_list and skills table."""
        for url in dic_scrap_profile:
            for skill in dic_scrap_profile[url][SKILLS][DATA]:
                skill_name = 'Nan'
                skill_level = 'Nan'

                try:
                    skill_name = list(skill.keys())[0]
                except:
                    pass

                try:
                    skill_level = skill[skill_name]
                except:
                    pass

                self.cur.execute(INSERT_SKILLS_NAME, [skill_name])

                self.cur.execute(SELECT_ID_SKILLS, [skill_name])

                id_skill = self.cur.fetchone()[0]

                self.cur.execute(INSERT_SKILLS, [url, id_skill, skill_level])
        self.con.commit()

    def close(self):

        self.con.close()


if __name__ == "__main__":
    print("All tests passed")
