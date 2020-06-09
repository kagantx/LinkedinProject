
import requests
from bs4 import BeautifulSoup
from collections import Counter
class WebPage:
    def __init__(self,url,field_dictionary):
        self.url=url
        self.field_dictionary=field_list
    def get_data(self):
        """field_list is a list of lists with each top list being a category"""
        page=requests.get(url)
        counter_list=[]
        counter_list.append()
        soup=BeautifulSoup(page.text,'html.parser')

        print(soup.prettify())
        data_dictionary=[]
        for tag,text in field_list:
            field_text=
            data_dictionary.append(field_name:(field_text,get_wordcount_dictionary(field_text))
        return data_dictionary

    def get_wordcount_dictionary(self):
        """Obtains word list from file text, after filtering out punctuation"""
        file_fixed = re.sub(r'[!@:#$_.*;&"`,\]\[?\-()]', ' ', file_text)
        # Remove pronunciation marks that are never part of a word
        file_fixed_two = re.sub(r'\s\'', ' ', file_fixed)
        file_fixed_three = re.sub(r'\'\s', ' ', file_fixed_two)
        # Remove leading and trailing apostrophes, but not those inside words
        return Counter(file_fixed_three.lower().split())
        # Return a counter object of the words, with all words in lowercase
if __name__=='__main__':
    url_test="https://www.linkedin.com/jobs/view/1876270330/?alternateChannel=search
    WebPage()
    print("All tests passed")





