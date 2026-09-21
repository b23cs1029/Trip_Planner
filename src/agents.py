from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

model_name = "gemma2-9b-it"

def country_extractor(user_query):
    prompt = f"The user query is :- {user_query}.\n Output only the city, state or country name."
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
        {
            "role": "system",
            "content": "You are a Country, State or City extractor. You will get a prompt to plan a trip somewhere. You have to return the country, state or city in which user wants to go. Only return the name of the city, state or country in your response and nothing else. If there are multiple cities or multiple states or multiple countries then select the first place provided by user."
        },
        {
            "role": "user",
            "content": prompt
        }
        ],
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response.strip('\n ')

def cities_decider(user_query, cities_list):
    prompt = f"The user wants: {user_query}\nHere is a cities data where I am providing city name with its alternate name and a little about the city if available:\n"
    for i, city in enumerate(cities_list):
        prompt+= f"{i+1}. {city['name']} ({city['alt_name']}) :- {city['description']}\n"
    prompt += """Your response should be all the cities with their description as provided priority wise. Dont give anything else. Include all the cities provided in the prompt but priority wise."""
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
        {
            "role": "system",
            "content": "You are a trip planner city recommender. You will be given a list of cities or a single city and a user prompt. You have to recommend the user for which cities to visit. You have to do this task by analysing the user input and see which cities aligns with the user's interest and then prepare a priority wise order list. If you get only 1 city then return your response as that city only."
        },
        {
            "role": "user",
            "content": prompt
        }
        ],
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response.strip('\n').split('\n')

def hotels_selector(all_hotels, user_query):

    prompt = f"The user query is:- {user_query}\n. Hotels in one of the city are:-\n"
    for hotel_info in all_hotels:
        prompt += f"Name of the hotel:- {hotel_info["name"]}  "
        prompt += f"Review score word:- {hotel_info["reviewScoreWord"]}  "
        prompt += f"Review score:- {hotel_info["reviewScore"]}  "
        prompt += f"Price per night:- {hotel_info["rate"]}  "
        prompt += f"Check-In Time:- {hotel_info["checkIn_Time"]}  "
        prompt += f"Check-Out Time:- {hotel_info["checkOut_Time"]}\n\n"

    pormpt += "Select the best 5-6 hotels according to user's need and provide the hotel with all its information as provided."

    completion = client.chat.completions.create(
        model=model_name,
        messages=[
        {
            "role": "system",
            "content": "You are a trip hotel recommendor. You will be given some hotels in a particular city with details like 'hotel name', 'review word', 'review score(rating)', 'price per night', 'In Time', 'Out Time' of every hotel and a user query. You have to analyse that user query and recommend the hotels. For example if user wants budget friendly trip then recommend him best options in cheap hotels else go rating wise."
        },
        {
            "role": "user",
            "content": prompt
        }
        ],
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response.strip('\n').split('\n')

def manager(final_city_list, visiting_places, hotels, file_location, user_query, arrival_date):

    with open(file_location, "w", encoding="utf-8") as file:
        file.write("User Query: " + user_query + '\n' + "Arrival Date: " + arrival_date + '\n\n')

    for city in final_city_list:
        places_to_visit = visiting_places[city]
        all_hotels = hotels[city]

        prompt = f"The user query is:- {user_query}\n. Visiting places in the city- '{city}' are:-\n"
        for place in places_to_visit:
            prompt += place + '\n'
        prompt += "Hotels data in this city:-\n"
        prompt += hotels_selector(all_hotels, user_query)
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
            {
                "role": "system",
                "content": """You are a trip planner ummariser. You will be given a city name, visiting places in that city and hotels in that city. You have to return your output in the following format:-

                City: <given city name in prompt>
                ----Visiting Places(all visiting places in the city provided with very short description)
                        <place 1> : <short description>
                        <place 2> : <short description>...
                ----Recommended Hotels(all the hotels provided with all the details)
                        <hotel 1 name> : <all details>
                        <hotel 2 name> : <all details>...

                Put everything in very good format. Strictly follow this format. There should be not extra things like '*'."""
            },
            {
                "role": "user",
                "content": prompt
            }
            ],
            temperature=0.7,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        final_response =  response.strip('\n').split('\n')
        with open(file_location, "a", encoding="utf-8") as file:
            file.write(final_response + '\n\n')