from bs4 import BeautifulSoup
import requests
import json

# URLs to the dining menus
SPECIAL_MENU_URL = 'https://www.rit.edu/fa/diningservices/daily-specials'
GEN_MENU_URL = 'https://www.rit.edu/fa/diningservices/general-menus'

def get_special_menu_json():

    # Sets up the BeautifulSoup object
    page = requests.get(SPECIAL_MENU_URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    # All the content is stored in a div with class 'ds-ouput'
    html_content = soup.find('div', class_='ds-output')

    # Initiates the nested loops starting with location
    location_divs = get_locations(html_content)
    full_json = {'locations': get_locations_json(location_divs)}

    return full_json
    

def get_locations(content_div):
    """
    Returns the location divs from the content block
    :param: content_div - the parent div that has all the location divs
    """

    # the first element which is an empty div
    return content_div.findAll('div', recursive=False)[1:]

def get_locations_json(location_divs):

    json_list = []

    for location_div in location_divs:
        # Setup json
        location_json = {}

        # Get the attribtues
        location_name = location_div.find('h3').text
        
        meal_category_divs = get_meal_categories(location_div)
        location_categories = get_meal_categories_json(meal_category_divs)

        # Add attributes to json
        location_json['name'] = location_name
        location_json['categories'] = location_categories

        json_list.append(location_json)

    return json_list

def get_meal_categories(location_div):

    # Contains the meals and dishes of the location
    meals_list = location_div.find('div', class_='ds-loc-title')
    if meals_list.contents:
        return meals_list.findChildren(recursive=False)
    else:
        return []

def get_meal_categories_json(meal_category_divs):

    json_list = []

    for category_div in meal_category_divs:

        if category_div.contents:
            # Setup json
            category_json = {}

            # Get the attribtues
            category_name = category_div.find('div', class_='menu-type').text[:-5]
            station_divs = get_stations(category_div)
            category_stations = get_stations_json(station_divs)

            # Add attributes to json
            category_json['name'] = category_name
            category_json['stations'] = category_stations

            json_list.append(category_json)

    return json_list

def get_stations(meal_category_div):
    return meal_category_div.findAll('div', class_='col-xs-12 col-md-6 menu-category-list')

def get_stations_json(station_divs):

    json_list = []
    
    for station_div in station_divs:
        # Setup json
        station_json = {}

        # Get the attributes
        station_name = station_div.find('div', class_='menu-category').text
        station_items = get_station_items(station_div)
        
        # Add attributes to json
        station_json['name'] = station_name
        station_json['items'] = station_items

        json_list.append(station_json)

    return json_list

def get_station_items(station_div):
    
    station_items = []
    items = station_div.find('div', class_='menu-items').contents

    for item in items[:-1]:  # there is a new line at the end
        if str(item) != '<br/>':
            station_items.append(item)


    return station_items