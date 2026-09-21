import agents as agents
import web_scrapper as web_scrapper
import api_caller as api_caller
import utilis.city_selector as city_selector

user_query = input("Enter your trip information:- ")
arrival_date = input("Enter arrival date:- ")

country = agents.country_extractor(user_query)
cities = web_scrapper.get_top_cities_from_wikivoyage(country)
cities_list = agents.cities_decider(user_query, cities)
final_city_list = city_selector.final_city_list(cities, cities_list)
visiting_places = web_scrapper.visiting_places_extractor(final_city_list)
hotels = api_caller.search_hotels(final_city_list, arrival_date)
agents.manager(final_city_list, visiting_places, hotels, f"tests/Trip_to_{country}.txt", user_query, arrival_date)