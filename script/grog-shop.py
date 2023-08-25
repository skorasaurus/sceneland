import requests
from bs4 import BeautifulSoup 
import json
from collections import OrderedDict

session = requests.Session()
page = session.get('https://grogshop.gs/index.php', headers={'User-Agent': 'Mozilla/5.0'})

soup = BeautifulSoup(page.content, "html.parser")
calendar = soup.find(id="tw-responsive")
shows = calendar.find_all("div", class_="tw-section")

all_shows_list = []

for show in shows:
  all_shows_data = {} 
  headliner = show.find("div", class_="tw-name")
  opener = show.find("div", class_="tw-opening-act")
  sold_out = show.find("a", class_="tw_soldout")
  date = show.find("span", class_="tw-event-date")
  
  headlinerz = headliner.text.strip().replace("w / ", ", ").replace("w/ ", ", ").replace(" / / ", ", ").replace(" // ", ", ").replace(" / ", ", ").replace(" - ", ": ").replace(" – ", ": ")
  artists_with_openers = [headlinerz + ", " + opener.text.strip().replace("w/ ", "").replace(" / ", ", ")]

  # Create an ordered dictionary to store unique artist names
  unique_artists_dict = OrderedDict()

  # Process each entry in the list
  for entry in artists_with_openers:
      artists = entry.split(', ')  # Split by comma and space
      for artist in artists:
          artist = artist.strip()  # Remove leading/trailing spaces
          if artist:  # Skip empty entries
              unique_artists_dict[artist] = None  # Using dict keys to maintain order

  # Convert the ordered dictionary keys back to a list
  artists_with_openers_clean = list(unique_artists_dict.keys())

  if opener.text.strip() == "":
    all_shows_data['artist'] = [headlinerz]
  else:
    all_shows_data['artist'] = artists_with_openers_clean
  for link_element in show.findAll("a"):
    if link_element.parent == headliner:
      all_shows_data['link'] = link_element["href"]
  if sold_out:
    all_shows_data['sold_out'] = True
  dateFormatted = date.text.strip().replace("Aug ", "2023-08-").replace("Sep ", "2023-09-").replace("Oct ", "2023-10-").replace("Nov ", "2023-11-").replace("Dec ", "2023-12-").replace("Jan ", "2024-01-").replace("Feb ", "2024-02-").replace("Mar ", "2024-03-").replace("Apr ", "2024-04-").replace("May ", "2024-05-").replace("Jun ", "2024-06-").replace("Jul ", "2024-07-").replace("Mon, ", "").replace("Tue, ", "").replace("Wed, ", "").replace("Thu, ", "").replace("Fri, ", "").replace("Sat, ", "").replace("Sun, ", "").replace(", 2023", "").replace(", 2024", "") + "T20:00:00"
  all_shows_data['date'] = dateFormatted.replace("-1T", "-01T").replace("-2T", "-02T").replace("-3T", "-03T").replace("-4T", "-04T").replace("-5T", "-05T").replace("-6T", "-06T").replace("-7T", "-07T").replace("-8T", "-08T").replace("-9T", "-09T")
  all_shows_data['venue'] = "Grog Shop"
  all_shows_list.append(all_shows_data)

all_shows_json = json.dumps(all_shows_list, indent=2)
print(all_shows_json)
