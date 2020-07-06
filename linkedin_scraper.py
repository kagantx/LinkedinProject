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
import click
from constants import *


@click.command()
@click.argument('email')
@click.argument('password')
@click.option('--job', '-j', help='Which job type to search for', default=DEFAULT_JOB, show_default=True)
@click.option('--location', '-l', help='Location to search for jobs', default=DEFAULT_LOCATION, show_default=True)
@click.option('--nb_pages', '-n', help='How many pages to scrape', default=DEFAULT_PAGES_TO_SCRAPE, show_default=True)
@click.option('--sections', '-s',
              help='Sections to scrape. Please use single letters for E(x)perience (E)ducation (S)kills without spaces in any order',
              default='xes')
def main(email, password, job, location, nb_pages, sections):
    """Sanitizes inputs and then calls the Parser if input is OK"""
    if nb_pages < 1:
        raise ValueError(NO_PAGES_REQUESTED)
    section_set=set([character for character in sections])
    if not section_set.issubset(SECTION_DICT.keys()):
        raise ValueError(INVALID_SECTION_REQUESTED.format(sections))
    sections=[SECTION_DICT[sec] for sec in section_set]

    bot = LinkedinBot(email, password, job=job, location=location, nb_pages=nb_pages, sections=sections)
    bot.login()
    bot.scrape_url_profiles()
    bot.save_result()
    bot.load_result()


main()
