import requests
from bs4 import BeautifulSoup
import json

def scrape_ref(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # select table
    table = soup.find('table', {'class': 'footable countrytab'})
    satellites = []

    # Iterate through each row (exclude the header)
    rows = table.find_all('tr')[1:]
    for row in rows:
        cells = row.find_all('td')
        if cells:
            # extract name and href
            link = cells[0].find('a')
            href = link['href']

            satellites.append(href)

    return satellites


def scrape_satellite_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # select the element containing the satellite information
    section = soup.find(id='satinfo')
    
    # structure checking
    # print(section.prettify())
    
    
    # initialize satellite data to be passed to
    """
    1. NAME
    2. CLASS
    3. NORAD ID
    4. INT'L CODE
    5. PERIGEE
    6. APOGEE
    7. INCLINATION
    8. PERIOD
    9. SEMI MAJOR AXIS
    10. RCS
    11. LAUNCH DATE
    12. SOURCE
    13. LAUNCH SITE
    14. DESCRIPTION
    """ 
    sat_data = {}

    name = section.find('h1').text.strip()
    sat_data["name"] = name

    try:
        sat_class = section.find('li', class_="arrow").find('a').text.strip()
        sat_data["sat_class"] = sat_class
    except:
        sat_data["sat_class"] = 0

    fields = [
        ("norad_id", "NORAD ID"),
        ("intl_code", "Int'l Code"),
        ("perigee", "Perigee"),
        ("apogee", "Apogee"),
        ("inclination", "Inclination"),
        ("period", "Period"),
        ("semi major axis", "Semi major axis"),
        ("rcs", "RCS"),
        ("launch_date", "Launch date"),
        ("source", "Source"),
        ("launch_site", "Launch site"),
    ]

    for field, label in fields:
        try:
            if label == "Launch date":
                value = section.find('b', string=label).find_next('a').text.strip()
            else:
                value = section.find('b', string=label).next_sibling.text.strip(": ").strip()
            sat_data[field] = value
        except:
            sat_data[field] = 0
    
    try: 
        all_texts = [element.strip() for element in section.stripped_strings]
        all_texts = [text for text in all_texts if text]

        description_candidates = []
        for text in reversed(all_texts):
            if "Launch" not in text and "NORAD" not in text and "Source" not in text:
                description_candidates.append(text)
            else:
                # Stop once we encounter launch-related or other technical info
                break
        
        sat_data["description"] = description_candidates[0] if description_candidates else 0
    except:
        sat_data["description"] = 0
    
    validate_description(sat_data)
    return sat_data
    
def validate_description(satellite_data: dict):
    if satellite_data["description"] == 0:
        return
    
    description = satellite_data.get('description', '').strip()
    launch_site = satellite_data.get('launch_site', '').strip()

    if description == f": {launch_site}" or description == launch_site:
        satellite_data["description"] = 0

url = "https://www.n2yo.com/satellites/?c=INDO&t=country"
satellite_links = scrape_ref(url)

""" href scrapper is fixed """
#print(satellite_data)

satellite_data = []

""" satellite data scrapper is fixed """
for href in satellite_links:
    domain = "https://www.n2yo.com"
    data = scrape_satellite_data(domain+href)
    # satellite_data.append(data)
    satellite_data.append(data)

with open("infoboard.json", "w") as f:
    json.dump(satellite_data, f, indent=4)