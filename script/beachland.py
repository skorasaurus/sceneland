import requests
from bs4 import BeautifulSoup 
import json

# Load the page
session = requests.Session()
page = session.get('https://www.beachlandballroom.com/', headers={'User-Agent': 'Mozilla/5.0'})

# Grab the container elements in the DOM
soup = BeautifulSoup(page.content, "html.parser")
calendar = soup.find("div", class_="up")
shows = calendar.find_all("article", class_="list-view-item")

# An empty array as a place to save the output
all_shows_list = []

# Iterate through the events in the DOM
for show in shows:
  # Empty object for each show, to be populated below
  all_shows_data = {} 
  # Get the artist container element
  artists_span = show.find_all("span", class_="tw-artist")
  # Get the date container element
  date_span = show.find("span", class_="event-date")
  # Iterate through all artists
  for artist_span in artists_span:
    # Get headlining and supporting acts as plaintext
    all_shows_data['artist'] = artist_span.text.strip()
  # Get the date as plaintext and format it as YYYY-MM-(D)D
  all_shows_data['date'] = date_span.text.strip().replace("\n", " ").replace("Aug ", "2023-08-").replace("Sep ", "2023-09-").replace("Oct ", "2023-10-").replace("Nov ", "2023-11-").replace("Dec ", "2023-12-").replace("Jan ", "2024-01-").replace("Feb ", "2024-02-").replace("Mar ", "2024-03-").replace("Apr ", "2024-04-").replace("May ", "2024-05-").replace("Jun ", "2024-06-").replace("Jul ", "2024-07-").replace("Monday ", "").replace("Tuesday ", "").replace("Wednesday ", "").replace("Thursday ", "").replace("Friday ", "").replace("Saturday ", "").replace("Sunday ", "")
  # Add the venue name
  all_shows_data['venue'] = "Beachland"
  # Populate the empty array `[]` with the object we just defined
  all_shows_list.append(all_shows_data)

# Make our final list more readable with JSON formatting
# This is technically a Python string, but we don’t care about that anymore
all_shows_json = json.dumps(all_shows_list, indent=2) 
print(all_shows_json)
