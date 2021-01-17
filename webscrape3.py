import requests
from bs4 import BeautifulSoup
import pandas as pd

# from web_scraper import driver

URL = 'https://ojp.nationalrail.co.uk/service/timesandfares/NRW/IPS/today/1545/dep/200121/1745/dep'
page = requests.get(URL)

# driver.quit()
class CheapestTicket():
    def __init__(self, url, isReturn):
        self.url = url
        self.isReturn = isReturn

    def find_cheapest_ticket(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='oft')
        trains = results.find_all(class_='mtx')

        Trains_list = []
        # print(trains[0])
        # for train in trains:
        #     print(train, end='\n'*2)
        if (self.isReturn is True):
            return trains[0].find(class_='opreturn').text.strip()
        else:
            return trains[0].find(class_='opsingle').text.strip()

