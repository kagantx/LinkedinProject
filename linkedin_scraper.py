"""
Command line interface for LinkedIn scraper.
Calls linkedin_base.py to do a scraping job after validating inputs.

Contains main() function and click decorators

Uses constants
SECTION_DICT dictionary from letter inputs to sections to scrape
NO_PAGES_REQUESTED - Error message if no pages were requested for scraping
INVALID_SECTION_REQUESTED - Error message if an invalid section was requested

DEFAULT_JOB
DEFAULT_LOCATION
DEFAULT_PAGES_TO_SCRAPE

"""

from linkedin_base import LinkedinBot
from linkedin_database import LinkedinDatabase
import click
import sys

from constants import *
from linkedin_logger import getmylogger

logger = getmylogger(__name__)


@click.command()
@click.argument('email')
@click.argument('password')
@click.option('--job', '-j', help='Which job type to search for', default=DEFAULT_JOB, show_default=True)
@click.option('--location', '-l', help='Location to search for jobs', default=DEFAULT_LOCATION, show_default=True)
@click.option('--nb_pages', '-n', help='How many pages to scrape', default=DEFAULT_PAGES_TO_SCRAPE,
              type=click.IntRange(1, None), show_default=True)
@click.option('--db_filename', '-d', help='Name of database file',
              default=DEFAULT_DB_FILENAME, show_default=True)
@click.option('--new_db/--keep_db', help='Whether to overwrite the database', default=False)
@click.option('--sections', '-s',
              help=SECTIONS_HELP,
              default=SECTION_LETTERS_DEFAULT)
def main(email, password, job, location, nb_pages, db_filename, sections, new_db):
    """Sanitizes inputs and then calls the Parser if input is OK"""
    section_set = set([character for character in sections])
    if not section_set.issubset(SECTION_DICT.keys()):
        logger.critical(INVALID_SECTION_REQUESTED.format(sections))
        sys.exit(1)
    sections = [SECTION_DICT[sec] for sec in section_set]

    db_bot = LinkedinDatabase(job=job, location=location, database_file=db_filename)

    bot = LinkedinBot(email, password, job=job, location=location, nb_pages=nb_pages, sections=sections,
                      database=db_bot)
    if new_db:
        db_bot.remove_db()
    db_bot.create_db()

    bot.login()
    bot.get_profile_urls()
    bot.scrape_content_profiles()
    bot.export_scrapes()
    # db_bot.insert_data()


if __name__ == '__main__':
    main()
