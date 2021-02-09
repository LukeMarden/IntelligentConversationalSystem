import requests
from bs4 import BeautifulSoup
# ************************************************************************************************************
#
#
#    webscrape3.py
# This class is used to webscrape the cheapest ticket
#
#
#    By: Group 18
#
#    Created: 03/01/2021
#
# ************************************************************************************************************
class CheapestTicket():

    # This method is used to initialise the classes variables
    # url: The url to scrape from
    # isReturn: whether the ticket is a return or not
    def __init__(self, url, isReturn):
        self.url = url
        self.isReturn = isReturn

    # This method finds the cheapest ticket
    # return: The cheapest ticket price
    def find_cheapest_ticket(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='oft')
        trains = results.find_all(class_='mtx')

        if (self.isReturn is True):
            return trains[0].find(class_='opreturn').text.strip()
        else:
            return trains[0].find(class_='opsingle').text.strip()

