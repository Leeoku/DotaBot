import json

with open('heroes.json') as json_file:
    data = json.load(json_file)
    heroes = []
    for name in data['heroes']:
        #Take the common name of the hero from the dictionary and add to heroes list
        heroes.append((name['localized_name'].lower()))
    heroes.sort()

#Ensure hero name passed is lowered for consistency
def is_valid_hero(hero_name):
    #return (hero_name in heroes)
    if any(hero_name in s for s in heroes):
        return True
    else:
        return False

def filter_hero(hero_name):
    filtered_heroes = []
    for e in heroes:
        if hero_name in e:
            filtered_heroes.append(e)
    return filtered_heroes
    # if len(filtered_heroes) == 1:
    #     return filtered_heroes[0]
    # elif len(filtered_heroes) == 0:
    #     return False
    # else:
    #     return "multiple", filtered_heroes