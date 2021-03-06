<<<<<<< HEAD
import json
from discord.ext import commands
import importlib
from helpers.helpfunctions import is_valid_hero, filter_hero
import helpers.helpfunctions
from helpers.dbase import Doto
import discord
import d2api
from d2api.src import entities
from helpers.api_key import cluster
import re
from datetime import datetime
import pymongo
import requests
from helpers.colour import green, red, yellow, blue, purple, endc, bold, underline
from bs4 import BeautifulSoup

db = cluster["leeoku"]
collection = db['dota']

timestamp = datetime.utcnow()

# @Person, Dota_Name, Dota_Id, Steam_Id (priority)
# !hero [hero] shows general information about selected hero (priority)
# !register [User_Id] links users discord to dota id (priority)
# !deregister [Discord_Id] removes link between user and dota id (priority)
# !leaderboard [User_Id] {global/server/bot/friends} shows leaderboad of selected info (future)
# !info [User_Id/Discord] shows general information about user (priority)
# !recent_games [User_Id] shows recent game info for user (future)
# !myprofile [User_Id] shows best heros, along with info for them, for selected user (priority)
# !my_items {uses/wins/kd/econ} best items for selected filter/user (future)

async def tracker(name):
    name = name.replace("#", "%23")
    URL = f'https://steamidfinder.com/lookup/{name}/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    job = soup.find('div', class_="panel-body")
    test = str(job)
    check_for_number = re.compile(r'\d+')
    num_output = check_for_number.findall(test)
    try:
        print(int(num_output[7]))
        return num_output[7]
    except IndexError:
        await ctx.send('Cannot find user. Make sure profile is publically displayed')

class HeroCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        importlib.reload(helpers.helpfunctions)

    @commands.command()
    async def hero(self, ctx, *, arg=None):
        print ("Given arg: ", arg)
        print(filter_hero(arg))
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        async def get_message():
            return (await self.bot.wait_for('message', check=check, timeout = 10)).content
            
        if not arg:
            print (f"Arg was {type(arg)}")
            await ctx.send(f"Please enter hero!")
            return

        arg = arg.lower()

        if len(filter_hero(arg)) == 1:
            filter_hero_name = filter_hero(arg)[0]
            dotabuff_hero_name = filter_hero_name.replace(" ", "-").lower()
            dotawiki_hero_name = filter_hero_name.replace(" ","_").title()
            dotabuff_link = f"https://www.dotabuff.com/heroes/{dotabuff_hero_name}"
            dotawiki_link = f"https://dota2.gamepedia.com/{dotawiki_hero_name}"
            await ctx.send(f'Dotabuff: {dotabuff_link}\n DotaWiki: {dotawiki_link}') # s
            return
            
        # If length of filter hero is greater than 1. So we have multiple matches
        # i.e ['chaos knight', 'dragon knight', 'omniknight']
        elif len(filter_hero(arg)) > 1:
            final_hero = []
            while len(final_hero) != 1:
                await ctx.send(f"Please narrow your search for:\n**{', '.join(filter_hero(arg))}**")
                get_hero = await get_message()
                if get_hero in filter_hero(arg):
                    final_hero.append(get_hero)
                    pass
            dotabuff_hero_name = get_hero.replace(" ", "-").lower()
            dotawiki_hero_name = get_hero.replace(" ","_").title()

            dotabuff_link = f"https://www.dotabuff.com/heroes/{dotabuff_hero_name}"
            dotawiki_link = f"https://dota2.gamepedia.com/{dotawiki_hero_name}"

            await ctx.send(f'Dotabuff: {dotabuff_link}\n DotaWiki: {dotawiki_link}') 
            return

        else: # No matched heros
            await ctx.send('No matched heroes')

    @commands.command()
    async def addhero(self, ctx, *, heroname):
        get_user = await Doto().by_id(ctx.author.id).get()
        current_heroes = [x.lower() for x in get_user['top_5_heroes']]
        print(heroname)
        #Determine if hero name is valid
        if is_valid_hero(heroname.lower()) == False:
            return await ctx.send("Not a valid hero")
        #Check duplicates
        if heroname.lower() in current_heroes:
            return await ctx.send('Hero already in pool')
        #Check to see if more than 5 heroes
        if len(current_heroes) >= 5:
            return await ctx.send('You have already assigned 5 heroes to yourself')
        #Validates if user registered, then adds hero
        if get_user:
            get_user['top_5_heroes'].append(heroname.title())
            await Doto().by_id(ctx.author.id).update(get_user)
            return await ctx.send(f"**{heroname.title()}** has been added to your pool of heroes")
        #Message if user not registered
        return await ctx.send('Please Register First')

    @commands.command()
    async def delhero(self, ctx, *, heroname):
        get_user = await Doto().by_id(ctx.author.id).get()
        current_heroes = [x.lower() for x in get_user['top_5_heroes']]
        #Determine if hero name is valid
        if is_valid_hero(heroname.lower()) == False:
            return await ctx.send("Not a valid hero")
        #Check to see if pool is empty
        if len(current_heroes) == 0:
            return await ctx.send('Current hero pool empty')
        #Validates if user registered
        if get_user:
            try:
                get_user['top_5_heroes'].remove(heroname.title())
            except ValueError:
                return await ctx.send((f"**{heroname.title()}** not in pool of heroes"))
            await Doto().by_id(ctx.author.id).update(get_user)
            return await ctx.send(f"**{heroname.title()}** has been removed from pool of heroes")
        #Message if user not registered
        return await ctx.send('Please Register First')

    @commands.command()
    async def myprofile(self, ctx):
        get_user = await Doto().by_id(ctx.author.id).get()
        print(len(get_user['top_5_heroes']))
        if len(get_user.get('top_5_heroes')) == 0:
            await ctx.send("Please add hero with **!addhero**")
        doto = '\n'.join(get_user['top_5_heroes'])
        #image = data['profile_image']
        embed = discord.Embed(title=get_user['steam_name'], description="Displaying data for user", colour=discord.Colour.teal(), timestamp=timestamp)
        embed.add_field(name = "Position", value = 0)
        embed.add_field(name="__**Top 5**__", value=doto)
        #embed.set_image(url=image)
        embed.set_footer(text="DotaBot")
        await ctx.send(embed=embed)

def setup(bot):
=======
import json
from discord.ext import commands
import importlib
from helpers.helpfunctions import is_valid_hero, filter_hero
import helpers.helpfunctions
from helpers.dbase import Doto
import discord
import d2api
from d2api.src import entities
from helpers.api_key import cluster
import re
from datetime import datetime
import pymongo
import requests
from helpers.colour import green, red, yellow, blue, purple, endc, bold, underline
from bs4 import BeautifulSoup

db = cluster["leeoku"]
collection = db['dota']

timestamp = datetime.utcnow()

# @Person, Dota_Name, Dota_Id, Steam_Id (priority)
# !hero [hero] shows general information about selected hero (priority)
# !register [User_Id] links users discord to dota id (priority)
# !deregister [Discord_Id] removes link between user and dota id (priority)
# !leaderboard [User_Id] {global/server/bot/friends} shows leaderboad of selected info (future)
# !info [User_Id/Discord] shows general information about user (priority)
# !recent_games [User_Id] shows recent game info for user (future)
# !myprofile [User_Id] shows best heros, along with info for them, for selected user (priority)
# !my_items {uses/wins/kd/econ} best items for selected filter/user (future)

#Check to see if username is a valid existing Steam username
async def tracker(name):
    name = name.replace("#", "%23")
    URL = f'https://steamidfinder.com/lookup/{name}/'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    job = soup.find('div', class_="panel-body")
    test = str(job)
    check_for_number = re.compile(r'\d+')
    num_output = check_for_number.findall(test)
    try:
        print(int(num_output[7]))
        return num_output[7]
    except IndexError:
        await ctx.send('Cannot find user. Make sure profile is publically displayed')

class HeroCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        importlib.reload(helpers.helpfunctions)

#Command to check a hero name
    @commands.command()
    async def hero(self, ctx, *, arg=None):
        print ("Given arg: ", arg)
        print(filter_hero(arg))
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        async def get_message():
            return (await self.bot.wait_for('message', check=check, timeout = 10)).content
            
        if not arg:
            print (f"Arg was {type(arg)}")
            await ctx.send(f"Please enter hero!")
            return

        arg = arg.lower()
        #Takes the arguement after lowering and matches it to the correct dotabuff hero syntax
        if len(filter_hero(arg)) == 1:
            filter_hero_name = filter_hero(arg)[0]
            dotabuff_hero_name = filter_hero_name.replace(" ", "-").lower()
            dotawiki_hero_name = filter_hero_name.replace(" ","_").title()
            dotabuff_link = f"https://www.dotabuff.com/heroes/{dotabuff_hero_name}"
            dotawiki_link = f"https://dota2.gamepedia.com/{dotawiki_hero_name}"
            await ctx.send(f'Dotabuff: {dotabuff_link}\n DotaWiki: {dotawiki_link}') # s
            return
            
        # If length of filter hero is greater than 1. So we have multiple matches
        # i.e ['chaos knight', 'dragon knight', 'omniknight']
        elif len(filter_hero(arg)) > 1:
            final_hero = []
            while len(final_hero) != 1:
                await ctx.send(f"Please narrow your search for:\n**{', '.join(filter_hero(arg))}**")
                get_hero = await get_message()
                if get_hero in filter_hero(arg):
                    final_hero.append(get_hero)
                    pass
            dotabuff_hero_name = get_hero.replace(" ", "-").lower()
            dotawiki_hero_name = get_hero.replace(" ","_").title()

            dotabuff_link = f"https://www.dotabuff.com/heroes/{dotabuff_hero_name}"
            dotawiki_link = f"https://dota2.gamepedia.com/{dotawiki_hero_name}"

            await ctx.send(f'Dotabuff: {dotabuff_link}\n DotaWiki: {dotawiki_link}') 
            return
        # No matched heros
        else: 
            await ctx.send('No matched heroes')

    @commands.command()
    async def addhero(self, ctx, *, heroname):
        get_user = await Doto().by_id(ctx.author.id).get()
        current_heroes = [x.lower() for x in get_user['top_5_heroes']]
        print(heroname)
        #Determine if hero name is valid
        if is_valid_hero(heroname.lower()) == False:
            return await ctx.send("Not a valid hero")
        #Check duplicates
        if heroname.lower() in current_heroes:
            return await ctx.send('Hero already in pool')
        #Check to see if more than 5 heroes
        if len(current_heroes) >= 5:
            return await ctx.send('You have already assigned 5 heroes to yourself')
        #Validates if user registered, then adds hero
        if get_user:
            get_user['top_5_heroes'].append(heroname.title())
            await Doto().by_id(ctx.author.id).update(get_user)
            return await ctx.send(f"**{heroname.title()}** has been added to your pool of heroes")
        #Message if user not registered
        return await ctx.send('Please Register First')

    @commands.command()
    async def delhero(self, ctx, *, heroname):
        get_user = await Doto().by_id(ctx.author.id).get()
        current_heroes = [x.lower() for x in get_user['top_5_heroes']]
        #Determine if hero name is valid
        if is_valid_hero(heroname.lower()) == False:
            return await ctx.send("Not a valid hero")
        #Check to see if pool is empty
        if len(current_heroes) == 0:
            return await ctx.send('Current hero pool empty')
        #Validates if user registered
        if get_user:
            try:
                get_user['top_5_heroes'].remove(heroname.title())
            except ValueError:
                return await ctx.send((f"**{heroname.title()}** not in pool of heroes"))
            await Doto().by_id(ctx.author.id).update(get_user)
            return await ctx.send(f"**{heroname.title()}** has been removed from pool of heroes")
        #Message if user not registered
        return await ctx.send('Please Register First')

    #Create a discord bot embed message with your profile info
    @commands.command()
    async def myprofile(self, ctx):
        get_user = await Doto().by_id(ctx.author.id).get()
        print(len(get_user['top_5_heroes']))
        if len(get_user.get('top_5_heroes')) == 0:
            await ctx.send("Please add hero with **!addhero**")
        doto = '\n'.join(get_user['top_5_heroes'])
        #image = data['profile_image']
        embed = discord.Embed(title=get_user['steam_name'], description="Displaying data for user", colour=discord.Colour.teal(), timestamp=timestamp)
        # embed.add_field(name = "Position", value = 0)
        embed.add_field(name="__**Top 5**__", value=doto)
        #embed.set_image(url=image)
        embed.set_footer(text="DotaBot")
        await ctx.send(embed=embed)

def setup(bot):
>>>>>>> c3f8b02994fac7da9602b70007a2be509c271521
    bot.add_cog(HeroCommand(bot))