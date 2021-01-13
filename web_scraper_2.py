import requests
from bs4 import BeautifulSoup
import pandas as pd

# from web_scraper import driver

URL = 'https://ojp.nationalrail.co.uk/service/timesandfares/NRW/IPS/today/1545/dep'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='oft')
trains = results.find_all(class_='mtx')

Trains_list = []
# print(trains[0])
# for train in trains:
#     print(train, end='\n'*2)
for train in trains:
    depart = train.find(class_='dep').text.strip()
    origin = train.find(class_='from').find(class_='result-station').text.strip()
    duration = train.find(class_='dur').text.strip()
    arrive = train.find(class_='arr').text.strip()
    Destination = train.find(class_='to').find(class_='result-station').text.strip()
    Faire = train.find(class_='opsingle').text.strip()
    Train_item = {
        'depart': depart,
        'origin': origin,
        'duration': duration,
        'arrive': arrive,
        'Destination': Destination,
        'Faire': Faire
    }

    Trains_list.append(Train_item)

df = pd.DataFrame(Trains_list)
print(df)
# driver.quit()