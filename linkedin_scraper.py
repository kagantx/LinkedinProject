from linkedin_base import LinkedinBot
import click


@click.command()
@click.argument('email')
@click.argument('password')
@click.option('--job', '-j', help='Which job type to search for', default='Data Scientist',show_default=True)
@click.option('--location', '-l', help='Location to search for jobs', default='New York',show_default=True)
@click.option('--nb_pages', '-n', help='How many pages to scrape', default=50,show_default=True)
def main(email, password, job, location, nb_pages):
    bot = LinkedinBot(email, password, job=job, location=location, nb_pages=nb_pages)
    bot.login()
    bot.scrape_url_profiles()
    bot.save_result()
    bot.load_result()

main()