import requests
from bs4 import BeautifulSoup

class CheapestTicket():
    def __init__(self, url, isReturn):
        self.url = url
        self.isReturn = isReturn

    def find_cheapest_ticket(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='oft')
        trains = results.find_all(class_='mtx')

        if (self.isReturn is True):
            return trains[0].find(class_='opreturn').text.strip()
        else:
            return trains[0].find(class_='opsingle').text.strip()

