from linkedin_base import LinkedinBot
import click
import sys

SECTION_DICT = {'x': "Experience", 'e': "Education", 's': "Skills"}


@click.command()
@click.argument('email')
@click.argument('password')
@click.option('--job', '-j', help='Which job type to search for', default='Data Scientist', show_default=True)
@click.option('--location', '-l', help='Location to search for jobs', default='New York', show_default=True)
@click.option('--nb_pages', '-n', help='How many pages to scrape', default=50, show_default=True)
@click.option('--sections', '-s',
              help='Sections to scrape. Please use single letters for E(x)perience (E)ducation (S)kills without spaces in any order',
              default='xes')
def main(email, password, job, location, nb_pages, sections):
    """Sanitizes inputs and then calls the Parser if input is OK"""
    if nb_pages < 1:
        raise ValueError("You must ask to scrape at least one page")
    section_set=set([character for character in sections])
    if not section_set.issubset(SECTION_DICT.keys()):
        raise ValueError("You asked us to scrape a section we cannot scrape")
    sections=[SECTION_DICT[sec] for sec in section_set]

    bot = LinkedinBot(email, password, job=job, location=location, nb_pages=nb_pages, sections=sections)
    bot.login()
    bot.scrape_url_profiles()
    bot.save_result()
    bot.load_result()


main()
