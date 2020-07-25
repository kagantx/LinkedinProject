from constants import *
import os
import sqlite3
import pickle
from linkedin_logger import getmylogger

logger = getmylogger(__name__)


class LinkedinDatabase:
    def __init__(self, job=DEFAULT_JOB, location=DEFAULT_LOCATION, database_file=DEFAULT_DB_FILENAME):
        self.job = job
        self.location = location
        self.database_file = database_file
        self.con = sqlite3.connect(self.database_file)
        self.cur = self.con.cursor()

    def create_db(self):
        """The function will create the database"""

        self.cur.execute(CREATE_PROFILES_TABLE)

        self.cur.execute(CREATE_INSTITUTION_TABLE)

        self.cur.execute(CREATE_SUBJECTS_TABLE)

        self.cur.execute(CREATE_SKILL_LIST_TABLE)

        self.cur.execute(CREATE_COMPANIES_TABLE)

        self.cur.execute(CREATE_EDUCATIONS_TABLE)

        self.cur.execute(CREATE_SKILLS_TABLE)

        self.cur.execute(CREATE_EXPERIENCES_TABLE)
        self.con.commit()
        logger.info("Created database tables successfully")

    def remove_db(self):
        if os.path.exists(self.database_file):
            os.remove(self.database_file)
            logger.info("Removed database tables successfully")

        else:
            logger.info(f"Do not find the database to removed: {self.database_file}")


if __name__ == "__main__":
    print("All tests passed")
