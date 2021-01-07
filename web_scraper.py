from urllib.request import urlopen
from bs4 import BeautifulSoup

url_to_scrape = "https://ojp.nationalrail.co.uk/service/planjourney/search"


request_page = urlopen(url_to_scrape)
page_html = request_page.read()
request_page.close()

html_soup = BeautifulSoup(page_html, 'html.parser')

cactus_items = html_soup.find_all('div', class_="jp-left")

filename = 'products.csv'
f = open(filename, 'w')

headers = 'Title, Price \n'

f.write(headers)

for cactus in cactus_items:
    A = cactus.find('div', class_="field half").text
    B = cactus.find('div', class_="field clear").text
    C = cactus.find('div', class_="no-float").text

    f.write(A + ',' + B + ',' + C)

f.close()

