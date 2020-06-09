from selenium import webdriver
from time import sleep


class LikenBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self):
        self.driver.get('https://www.linkedin.com/')

        # identification button
        login_btn_1 = self.driver.find_element_by_xpath('/html/body/nav/a[3]')
        login_btn_1.click()

        sleep(1)

        email_in = self.driver.find_element_by_xpath('//*[@id="username"]')
        email_in.send_keys('bensaid.lucas@gmail.com')

        pw_in = self.driver.find_element_by_xpath('//*[@id="password"]')
        pw_in.send_keys('261194')

        login_btn_2 = self.driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button')
        login_btn_2.click()

        sleep(1)

        # page with data scientist profile
        #self.driver.get('https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22il%3A0%22%5D&keywords=data%20scientist&origin=FACETED_SEARCH')
        self.driver.get('https://www.linkedin.com/search/results/people/?facetGeoRegion=%5B%22us%3A0%22%5D&keywords=data%20scientist&origin=FACETED_SEARCH')

        sleep(1)

    def next_page(self):
        next_page_btn = self.driver.find_element_by_xpath('//*[@id="ember1229"]/span')
        next_page_btn.click()


if __name__ == '__main__':
    bot = LikenBot()
    bot.login()
    bot.next_page()
