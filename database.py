import sqlite3
import os
import pickle
from constants import *

JOB_SEARCH = 'data scientist'
LOCATION_SEARCH = 'tlv'

if os.path.exists(DB_FILENAME):
    os.remove(DB_FILENAME)

"""Create the database"""

con = sqlite3.connect(DB_FILENAME)
cur = con.cursor()

cur.execute(''' CREATE TABLE `profiles` (
                  `url` varchar(255) PRIMARY KEY,
                  `search_job` varchar(255),
                  `search_location` varchar(255));

                ''')

cur.execute(''' CREATE TABLE `institutions` (
                  `id` integer PRIMARY KEY AUTOINCREMENT,
                  `name` varchar(255) UNIQUE

                );

                ''')

cur.execute(''' CREATE TABLE `subjects` (
                  `id` integer PRIMARY KEY AUTOINCREMENT,
                  `name` varchar(255) UNIQUE
                );

                ''')

cur.execute(''' CREATE TABLE `skill_list` (
                  `id` integer PRIMARY KEY AUTOINCREMENT,
                  `name` varchar(255) UNIQUE
                );

                ''')

cur.execute(''' CREATE TABLE `companies` (
                  `id` integer PRIMARY KEY AUTOINCREMENT,
                  `name` varchar(255) UNIQUE
                );

                ''')

cur.execute('''  CREATE TABLE `educations` (
                  `id` integer PRIMARY KEY AUTOINCREMENT,
                  `url` varchar(255),
                  `graduation_type` varchar(255),
                  `id_institution` integer,
                  `id_subject` integer ,
                  `date` datetime,
                  FOREIGN KEY (`url`) REFERENCES `profiles` (`url`),
                  FOREIGN KEY (`id_institution`) REFERENCES `institutions` (`id`),
                  FOREIGN KEY (`id_subject`) REFERENCES `subjects` (`id`)
                );

                ''')

cur.execute(''' CREATE TABLE `skills` (
                  `id` integer PRIMARY KEY AUTOINCREMENT,
                  `url` varchar(255),
                  `id_skill` int,
                  `n_endorsements` int,
                  FOREIGN KEY (`url`) REFERENCES `profiles` (`url`),
                  FOREIGN KEY (`id_skill`) REFERENCES `skill_list` (`id`)
                );

                ''')

cur.execute(''' CREATE TABLE `experiences` (
                  `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                  `url` varchar(255),
                  `id_company` integer,
                  `job_name` varchar(255),
                  `start_date` datetime,
                  `duration` datetime,
                  `location` varchar(255),
                  FOREIGN KEY (`url`) REFERENCES `profiles` (`url`),
                  FOREIGN KEY (`id_company`) REFERENCES `companies` (`id`)
                );

                ''')

"""Open pickle file"""
dbfile = open(PICKLE_FILENAME, 'rb')
db = pickle.load(dbfile)

"""Insert experiments"""

for url in db.keys():
    for experience in db[url]['Experience']['Data']:

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
            company_name = experience[job_name]['Company Name']
        except:
            pass

        try:
            location = experience[job_name]['Location']
        except:
            pass

        try:
            duration = experience[job_name]['Employment Duration']
        except:
            pass

        try:
            start_date = experience[job_name]['Dates Employed']

        except:
            pass

        if job_name in ['Title', 'Company Name']:
            job_name = 'Nan'

        cur.execute(''' INSERT OR IGNORE INTO companies(name) VALUES(?)''', [company_name])

        cur.execute('''SELECT id FROM companies WHERE name=(?)''', [company_name])

        id_company = cur.fetchone()[0]

        cur.execute(
            ''' INSERT OR IGNORE INTO experiences(url, id_company, job_name, start_date, duration, location)\
             VALUES(?,?,?,?,?,?)''',
            [url, id_company, job_name, start_date, duration, location])

    cur.execute(''' INSERT OR IGNORE INTO profiles(url,search_job,search_location) VALUES(?,?,?)''',
                [url, JOB_SEARCH, LOCATION_SEARCH])

"""Education"""

for url in db.keys():
    for education in db[url]['Education']['Data']:
        institution = 'Nan'
        Degree_Name = 'Nan'
        Field_Of_Study = 'Nan'
        Dates = 'Nan'
        try:
            institution = list(education.keys())[0]
        except:
            pass

        try:
            Degree_Name = education[institution]['Degree Name']
        except:
            pass

        try:
            Field_Of_Study = education[institution]['Field Of Study']
        except:
            pass

        try:
            Dates = education[institution]['Dates attended or expected graduation']
        except:
            pass

        cur.execute(''' INSERT OR IGNORE INTO institutions(name) VALUES(?)''', [institution])

        cur.execute('''SELECT id FROM institutions WHERE name=(?)''', [institution])
        id_institution = cur.fetchone()[0]

        cur.execute(''' INSERT OR IGNORE INTO subjects(name) VALUES(?)''', [Field_Of_Study])

        cur.execute('''SELECT id FROM subjects WHERE name=(?)''', [Field_Of_Study])
        id_subject = cur.fetchone()[0]

        cur.execute(
            ''' INSERT OR IGNORE INTO educations(url, graduation_type, id_institution, id_subject, date ) VALUES(?,?,?,?,?)''', \
            [url, Degree_Name, id_institution, id_subject, Dates])



"""Skills"""

for url in db.keys():
    for skill in db[url]['Skills']['Data']:
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

        cur.execute(''' INSERT OR IGNORE INTO skill_list(name) VALUES(?)''', [skill_name])

        cur.execute('''SELECT id FROM skill_list WHERE name=(?)''', [skill_name])

        id_skill = cur.fetchone()[0]

        cur.execute(''' INSERT OR IGNORE INTO skills(url,id_skill,n_endorsements) VALUES(?,?,?)''', \
                    [url, id_skill, skill_level])