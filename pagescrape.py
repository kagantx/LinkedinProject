
import requests
from bs4 import BeautifulSoup
from collections import Counter
class WebPage:

    def __init__(self,url,field_dictionary):
        self.url=url
        self.field_dictionary=field_dictionary
        self.data_dictionary={}
        self.
    def get_data(self):
        """Obtain a dictionary containing the text for each field name,as well as a
        counter object for each text"""
        page=requests.get(self.url)
        counter_list=[]
        counter_list.append()
        soup=BeautifulSoup(page.text)

        print(soup.prettify())
        self.data_dictionary= {}
        for field_name,field_content in self.field_dictionary.items():
            self.add_webitem(field_name,field_content)

    def add_webitem(self,field_name,field_content):
        s
        field_name: (field_name, self.get_wordcount_dictionary(field_name))}

    def get_wordcount_dictionary(self,text):
        """Obtains word list from file text, after filtering out punctuation"""
        file_fixed = re.sub(r'[!@:#$_.*;&"`,\]\[?\-()]', ' ', text)
        # Remove punctuation marks that are never part of a word
        file_fixed_two = re.sub(r'\s\'', ' ', file_fixed)
        file_fixed_three = re.sub(r'\'\s', ' ', file_fixed_two)
        # Remove leading and trailing apostrophes, but not those inside words
        return Counter(file_fixed_three.lower().split())
        # Return a counter object of the words, with all words in lowercase
if __name__=='__main__':
    url_test="https://www.linkedin.com/in/daniel-kagan-691b7b182/"
    WebPage(url_test,{'job_titles':[]})
    print("All tests passed")





