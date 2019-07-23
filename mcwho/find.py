from sys import modules, stdout
from bs4 import BeautifulSoup
import requests
import json
import re
import urllib
from itertools import islice

this = modules[__name__]
this.mcu_actors = None

def __load_data():
    if this.mcu_actors is None:
        with open("mcu.json", "r", encoding="utf-8") as data_file:
            this.mcu_actors = json.load(data_file)

def get_actor(actor_id):
    if not actor_id in this.mcu_actors:    
         return None
    return this.mcu_actors[actor_id]    

def __retrieve_actor_details(search_string):    
    actor_search_endpoint = f"https://www.imdb.com/find?q={search_string}&s=nm"
    actor_search_soup = BeautifulSoup(requests.get(actor_search_endpoint).content, 'html.parser')
    actor_results = actor_search_soup.find_all("td", class_="result_text")
    for actor_row in actor_results:        
        actor_id = re.search("(nm\d+)", actor_row.a["href"], re.IGNORECASE) 
        if actor_id is None: 
            continue
        
        yield {"id": actor_id.group(1), "name": actor_row.a.get_text(strip=True)}

def check_mcwho(search_string, output = stdout):    
    if re.match("nm\d+", search_string):
        output.write(f"Searching for actor ID directly."   )
        mcu_actor = get_actor(search_string)
        if not mcu_actor is None:   
            yield mcu_actor
    else:
        search_string = urllib.parse.quote(search_string)
        top_actor_matches = islice(__retrieve_actor_details(search_string), 25)        
        for actor in top_actor_matches:         
            output.write(f"\nSearching for {actor['name']} in the MCU...")
            mcu_actor = get_actor(actor["id"])
            if not mcu_actor is None:   
                yield mcu_actor
            else:
                output.write(' not found')

__load_data()