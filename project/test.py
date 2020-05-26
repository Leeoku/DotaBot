# # from helpers.colour import red, blue, purple, yellow, green, endc, underline, bold


# # print(f"{green}This is what end does{endc} {blue} It ends the colour {endc}\n\n"
# #       f"{bold}{underline}{yellow}Testing123{endc}")

# # 
# import d2api
# from d2api.src import entities
# from helpers.api_key import steam_api

# # Hero/Item/Ability information is available without having to specify a key
# # print(entities.Hero(67)['hero_name'])
# # print(entities.all_heroes)
# # print(entities.Item(208)['item_aliases'])
# # print(entities.Ability(6697)['ability_name'])

# # Use steam32/steam64 IDs interchangeably
# # steam_account = entities.SteamAccount(4294967295)
# # print(steam_account['id32'], steam_account['id64'])
# # print hero frequency by name

# api = d2api.APIWrapper(api_key = steam_api)

# # fetch latest matches
# #match_history = api.get_match_history()
# #print(match_history)
# #match_dets = api.get_match_details(5426881753)
# # player_info = api.get_player_summaries(steam_accounts=list(["76561198012042633", "76561198047020843"]))
# # player_info = api.get_player_summaries(account_ids=list(["86755115"]))
# # player_info1 = api.get_player_summaries(steam_accounts=["Leeoku"])
# # print(f"{player_info}\n")
# # print(player_info1)
# #print(match_dets['players'])
# snapbot = api.get_player_summaries(account_ids=["76561198012042633", "76561198047020843"])
# # match_history = api.get_match_history(account_id=76561198047020843)
# print(snapbot)
# # print(matche)
# # print(match_history)
# # get frequency of heroes played in the latest 100 games
# # heroes = {}

# # for match in match_history['matches']:
# #     for player in match['players']:
# #         hero_id = player['hero']['hero_id']
# #         if not hero_id in heroes:
# #             heroes[hero_id] = 0
# #         heroes[hero_id] += 1
# # for hero_id, freq in heroes.items():
# #     print(entities.Hero(hero_id)['hero_name'], freq)

# # #


import math
import asyncio
import discord
import copy
import regex
import colorgram
import random
import datetime
import io
import emoji
import aiohttp
from discord.ext import commands
from PIL import Image
import re
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from collections.abc import Sequence
from utils import is_int
import datetime
import requests
from bs4 import BeautifulSoup
import datetime
import re

# def tracker(name):
#       name = name.replace("#", "%23")
#       URL = f'https://steamidfinder.com/lookup/{name}/'
#       page = requests.get(URL)
#       soup = BeautifulSoup(page.content, 'html.parser')
#       job = soup.find('div', class_="panel-body")
#       test = str(job)
#       check_for_number = re.compile(r'\d+')
#       num_output = check_for_number.findall(test)
#       print(int(num_output[7]))

# tracker('mcowned')

def tracker(ids):
    # name = name.replace("#", "%23")
    URL = f'https://www.dotabuff.com/players/{ids}'
    page = requests.get(URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')

        print(soup)
        job = soup.find('div', class_="label")
        print(job)
    else:
        print (f"Page returned {page.status_code} instead of 200.")

# https://www.dotabuff.com/players/86755115
tracker(86755115)