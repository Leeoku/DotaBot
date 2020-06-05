import json

with open('heroes.json') as json_file:
    data = json.load(json_file)
    heroes = []
    for name in data['heroes']:
        #Take the common name of the hero from the dictionary and add to heroes list
        heroes.append((name['localized_name'].lower()))
    heroes.sort()

# def is_valid_hero(hero_name):
#     print(heroes)
#     if any(hero_name == s for s in heroes) == True:
#         return True
#     else:
#         return False
#     print(any(hero_name == s for s in heroes))

def is_valid_hero(hero_name):
    return any(hero_name == s for s in heroes )

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

# for x in ['', 'a', 'b', 'c', 'ab', 'bc', 'abc']:
#   print(x in 'abc')

# print('ac' in 'abc')`