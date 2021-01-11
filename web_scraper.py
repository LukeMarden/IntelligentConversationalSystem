from selenium import webdriver
import pandas as pd

url = 'https://ojp.nationalrail.co.uk/service/timesandfares/IPS/NRW/today/1545/dep'

driver = webdriver.Chrome()
driver.get(url)

videos = driver.find_elements_by_class_name('alt mtx')

video_list = []

for video in videos:
    title = video.find_element_by_xpath('.//*[@id="results-from"]').text
    views = video.find_element_by_xpath('.//*[@id="results-details"]/span[1]').text
    when = video.find_element_by_xpath('.//*[@id="fare "]/span[2]').text
    #print(title, views, when)
    vid_item = {
        'title': title,
        'views': views,
        'posted': when
    }

    video_list.append(vid_item)

df = pd.DataFrame(video_list)
print(df)