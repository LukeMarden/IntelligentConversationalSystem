import requests
from bs4 import BeautifulSoup
URL = 'https://ojp.nationalrail.co.uk/service/timesandfares/IPS/NRW/today/1545/dep'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='oft')
trains = results.find_all(class_='mtx')
# print(trains[0])
# for train in trains:
#     print(train, end='\n'*2)
for train in trains:
    depart = train.find(class_='dep').text.strip()
    origin = train.find(class_='result-station').text.strip()
    duration = train.find(class_='dur').text.strip()
    print(depart)
    print(origin)
    print(duration)
    print()