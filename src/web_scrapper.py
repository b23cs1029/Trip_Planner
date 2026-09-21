import requests
from bs4 import BeautifulSoup

def get_top_cities_from_wikivoyage(country):
    
    url = f"https://en.wikivoyage.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch {country}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    cities_section = soup.find(id="Cities")
    if not cities_section:
        cities_list = [{'name': country, "alt_name": None, "description": None}]
        return cities_list

    cities_list = []

    for sibling in cities_section.parent.find_next_siblings():
        if sibling.name == "ul":
            for li in sibling.find_all("li"):
                city = {}

                name_tag = li.select_one(".fn.org.listing-name a")
                city["name"] = name_tag.text.strip() if name_tag else None
                alt_name_tag = li.find("i")
                city["alt_name"] = alt_name_tag.text.strip() if alt_name_tag else None
                full_text = li.get_text(" ", strip=True)
                if "—" in full_text:
                    city["description"] = full_text.split("—", 1)[1].strip()
                else:
                    city["description"] = None

                cities_list.append(city)

    return cities_list

def visiting_places_extractor(cities):
    visiting_places = {}
    for city in cities:
        url = f"https://en.wikivoyage.org/wiki/{city}"

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the URL: {e}")
            exit()

        soup = BeautifulSoup(response.text, 'html.parser')

        see_header = soup.find('h2', id='See')

        if see_header:
            see_content = []
            for element in see_header.parent.find_next_siblings():
                if element.name == 'h2':
                    break
                see_content.append(element.get_text(strip=True, separator=' '))
            visiting_places[city] = see_content

        else:
            print("Could not find the 'See' section on the page.")
        
    return visiting_places