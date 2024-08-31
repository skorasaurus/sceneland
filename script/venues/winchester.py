import requests
from bs4 import BeautifulSoup 
import json
from datetime import datetime
from collections import OrderedDict

# url base https://thewinchestermusictavern.com/page/1 
url_base = 'https://thewinchestermusictavern.com/page/'

url_pages = [1, 2, 3]


for url_page in url_pages:
  url_concat = url_base + str(url_page)
  session = requests.Session()
  page = session.get(url_concat, headers={'User-Agent': 'Mozilla/5.0'})
  soup = BeautifulSoup(page.content, 'html.parser')
  calendar = soup.find("div", class_="tw-plugin-upcoming-event-list")
  shows = calendar.find_all("div", class_="tw-section")

  all_shows_list = []

  for show in shows:
    all_shows_data = {} 
    artist = show.find('div', class_='tw-name')
    all_shows_data['artist'] = [artist.text.strip().replace(' w/ ', ', ')]

    for link_element in show.findAll('a'):
        all_shows_data['link'] = link_element['href'.split('?', 1)[0]]

    sold_out = show.find('a', class_='tw_soldout')
    if sold_out:
        all_shows_data['sold_out'] = True

    date = show.find('span', class_='tw-event-date').text.strip()
    print(date)
    time = show.find('span', class_='tw-event-time').text.strip()
    date = datetime.strptime(date, '%B %d, %Y').date()
    time = datetime.strptime(time, '%I:%M %p').time()
    all_shows_data['date'] = str(date).split(' ', 1)[0] + 'T' + str(time)
    
    # 2024-12-08T18:30:0

    all_shows_data['venue'] = 'Winchester Tavern'
    all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2)
print(all_shows_json)
