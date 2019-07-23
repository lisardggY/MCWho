from sys import output
from bs4 import BeautifulSoup
import requests
import re
import json

def get_actors(movieId):
    credits_endpoint = "https://www.imdb.com/title/" + movieId + "/fullcredits"
    credits_soup = BeautifulSoup(requests.get(credits_endpoint).content,'html.parser')    
    actor_rows = credits_soup.select("table.cast_list>tr.even:not(:has(>td[id])),table.cast_list>tr.odd:not(:has(>td[id]))")
    for actor_row in actor_rows:
        actor_id = re.search(".*\/(nm\d+).*", actor_row.select("td:nth-of-type(2)>a")[0]["href"], re.IGNORECASE)        
        if actor_id is None:
            continue
        else:
            episode_toggle = actor_row.select("a.toggle-episodes")
            if episode_toggle:
                episode_toggle[0].decompose()
            actor_name = actor_row.select("td:nth-of-type(2)>a")[0].get_text(strip=True)            
            actor_role = actor_row.select("td.character")[0].get_text(strip=True)
            actor_name = ' '.join(actor_name.split())
            actor_role = ' '.join(actor_role.split())
            actor = {"id":actor_id.group(1), "name":actor_name, "role":actor_role}            
            yield actor

def load_mcu_actors(output = sys.output):
    has_more_pages = True
    current_page = 1
    films_or_shows = []
    while has_more_pages:
        mcu_endpoint = f"https://www.imdb.com/search/keyword/?keywords=marvel-cinematic-universe&mode=simple&page={current_page}"    
        soup = BeautifulSoup(requests.get(mcu_endpoint).content, 'html.parser')
        current_page_data = soup.find_all("img", class_="loadlate")
        if current_page_data:
            print(f"Found {len(current_page_data)} films/shows in page {current_page}")
            films_or_shows.extend(current_page_data)
            current_page += 1
        else:
            has_more_pages = False

    mcu_actors = {}

    for film_or_show in films_or_shows:  
        iteration = 0
        title = film_or_show["alt"]
        id = film_or_show["data-tconst"]    
        for actor in get_actors(id):
            iteration += 1    
            actorId = actor["id"]
            actorName = actor["name"]
            if not actorId in mcu_actors:
                mcu_actors[actorId] = {"id":actorId, "name":actorName, "roles":[]}
            mcu_actors[actorId]["roles"].append ({"id":id, "title": title, "role": actor["role"]})
            if iteration % 50 == 0:
                print (f"Scanned {len(mcu_actors)} actors in {films_or_shows.index(film_or_show) + 1} films")
                
    with open("mcu.json", 'w', encoding="utf-8") as outfile:
        json.dump(mcu_actors, outfile, indent=True)
        
        





