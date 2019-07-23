import sys
from mcwho.find import get_actor
from mcwho.find import check_mcwho

def __interactive_print_actor(actor_id, actor_name, output = sys.stdout):
    actor = get_actor(actor_id)
    if actor is None:    
        output.write(f"{actor_name} isn't in the MCU... yet.")
        return False        
    else:        
        output.write(f"{actor['name']} has most recently been in {actor['roles'][0]['title']} as {actor['roles'][0]['role']}")
        if len(actor["roles"]) > 1:
            show_all_roles = input("Show other roles? [yN]: ")
            if (show_all_roles.lower() in ["y", "yes"]):
                for role in actor["roles"][1:]:
                    print(f"{role['role']} in {role['title']}\n")
        return True

def interactive_search():
    while True:
        try:
            search_string = input("Who do you want to find? (Ctrl-Z to quit): ")
        except EOFError:
            break    
        
        for match in check_mcwho(search_string):
            if match is None:
                break
            if __interactive_print_actor(match["id"], match["name"]):
                keep_searching = input("\nKeep looking for other matching actors? [yN]: ")
                if not keep_searching.lower() in ["y", "yes"]:
                    break        


