# LinkedinProject

This project scrapes LinkedIn to find profiles of people with a given job title and location.

The default job title is Data Scientist

The default location is Tel Aviv

The default number of pages to scrape is 1

It extracts three sections:

The Experiences (jobs) section

The Education section

The Skills section.



We only scrape the top few skills from the third section, and it fails some proportion of the time.
We are always able to scrape the first two sections


The scraped data is dynamically added to a sqlite embedded database. The database plan is in the data_design.pdf file.

We also make use of the HIPO API at the link below:


http://universities.hipolabs.com/search?name=middle





### Prerequisites

The python packages required are listed in requirements.txt. The main package
used is selenium, which does all the scraping because LinkedIn is a highly dynamic website.

Your linkedin login information is a required input parameter to the script.

### Installing

To install, place all the files in a single directory and create an environment with all of the 
libraries in requirements.txt

### Execute

Run the linkedin_scraper.py file with appropriate command line arguments, put all the files in the same folder

## Built With

* Pycharm

## Authors

* **Daniel Kagan** -- [kagantx](https://github.com/kagantx)
* **Lucas Bensaid** -- [lucasbens](https://github.com/lucasbens)

See also the list of [contributors](https://github.com/kagantx/contributors) who participated in this project.


## Acknowledgments

* https://www.linkedin.com/pulse/how-easy-scraping-data-from-linkedin-profiles-david-craven/

* https://www.youtube.com/watch?v=d2GBO_QjRlo&t=106s

* https://github.com/Hipo/university-domains-list?ref=apilist.fun

