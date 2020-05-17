import json

with open('heroes.json') as json_file:
    data = json.load(json_file)
    heroes = []
    for name in data['heroes']:
        #Take the common name of the hero from the dictionary and add to heroes list
        heroes.append((name['localized_name'].lower()))
    heroes.sort()
