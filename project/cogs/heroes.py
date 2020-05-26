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

# @Person, Dota_Name, Dota_Id, Steam_Id
# .hero [hero] shows general information about selected hero
# .map [section] shows information about selected part of map
# .register [User_Id] links users discord to dota id
# .deregister [Discord_Id] removes link between user and dota id
# .leaderboard [User_Id] {global/server/bot/friends} shows leaderboad of selected info
# .info [User_Id/Discord] shows general information about user
# .recent_games [User_Id] shows recent game info for user 
# .my_heros [User_Id] shows best heros, along with info for them, for selected user
# .my_items {uses/wins/kd/econ} best items for selected filter/user

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

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        
        async def get_message():
            return (await self.bot.wait_for('message', check=check)).content
            
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
            await ctx.send(f"Please narrow your search for:\n**{', '.join(filter_hero(arg))}**")
            get_hero = await get_message()

            dotabuff_hero_name = get_hero.replace(" ", "-").lower()
            print(dotabuff_hero_name)

            dotawiki_hero_name = get_hero.replace(" ","_").title()
            print(dotawiki_hero_name)

            dotabuff_link = f"https://www.dotabuff.com/heroes/{dotabuff_hero_name}"
            dotawiki_link = f"https://dota2.gamepedia.com/{dotawiki_hero_name}"

            await ctx.send(f'Dotabuff: {dotabuff_link}\n DotaWiki: {dotawiki_link}') 
            return

        else: # No matched heros
            # await ctx.send(f"Please refine your search!")
            await ctx.send('No matched heroes')


    # @commands.command()
    # async def test(self, ctx):
    #     print(f"\nGUILD NAME: {ctx.guild}")
    #     print(f"\nGUILD ID: {ctx.guild.id}")
    #     print(f"\nAUTHOR ID: {ctx.author.id}")
    #     print(f"\nAUTHOR:{ctx.author}")
    #     print(f"\nCHANNEL ID: {ctx.channel.id}")


    @commands.command()
    async def addhero(self, ctx, *, hero):
        await ctx.send(f"**{hero}** Has been added to your pool of heroes.")     


    # @commands.command()
    # async def register(self, ctx, *, steam_name=None):
    #     if steam_name is None:
    #         await ctx.send('Enter your steam name')
    #         return
    #     payload = {
    #         '_id': ctx.author.id,
    #         'steam_name':steam_name,
    #         'pos': 0,
    #         'top_5_heroes': [],
    #         'least_5_heroes':[],
    #         'profile_image': ''
    #     }
    #     await Doto().create(payload)
    #     print(f'{green} User has been successfully entered into the data base{endc}')
    #     return

    @commands.command()
    async def addhero(self, ctx, *, heroname):
        get_user = await Doto().by_id(ctx.author.id).get()
        if len(get_user['top_5_heroes']) > 5:
            return await ctx.send('You have already assigned 5 heroes to yourself')
        if get_user:
            get_user['top_5_heroes'].append(heroname)
            await Doto().by_id(ctx.author.id).update(get_user)
            return await ctx.send(f"**{heroname}** has been added to your pool of heroes")
        return await ctx.send('Please Register First')

        # Add .deregister for admins
    @commands.command()
    async def myprofile(self, ctx):
        data = await Doto().by_id(ctx.author.id).get()
        print(data)
        doto = '\n'.join(data['top_5_heroes'])
        print(doto)
        doto2 = '\n'.join(data['least_5_heroes'])
        image = data['profile_image']

        embed = discord.Embed(title=data['steam_name'], description="Displaying data for user", colour=discord.Colour.teal(), timestamp=timestamp)
        embed.add_field(name="__**Top 6**__", value=doto)
        # embed.add_field(name="__**Least 5**__", value=doto2)
        embed.set_image(url=image)
        embed.set_footer(text="DotaBot")
        await ctx.send(embed=embed)

    # @commands.command()
    # async def profilepic(self, ctx, *, image):
    #     get_user = await Doto().by_id(ctx.author.id).get()
    #     get_user['profile_image'] = image
    #     await Doto().by_id(ctx.author.id).update(get_user)
    #     return await ctx.send('Profile image updated')


        # await ctx.send(f"User: {ctx.author.name}\n"
        #                f"Pos: #5\n"
        #                f"Hero Pool: Crystal Madien, Dazzle\n"
        #                f"Most Played Hero: Crystal Madien\n"
        #                f"Least Played Hero: Juggernaut")




    # @commands.command()
    # async def steamprofile(self, ctx, id: str):
    #     api = d2api.APIWrapper(api_key = steam_api)
    #     snapbot = api.get_player_summaries(account_ids=[f"{id}"])
    #     print(snapbot)
    #     find_number = str(snapbot['players'][0]['steam_account'])
    #     print(find_number)
    #     check_for_number = re.compile(r'\d+')
    #     num_output = check_for_number.findall(find_number)
    #     print(num_output[0])

    # @commands.command()
    # async def test(self, ctx, name: str):
    #     result = await tracker(name)
    #     api = d2api.APIWrapper(api_key = steam_api)
    #     snapbot = api.get_player_summaries(account_ids=[f"{result}"])
    #     print(snapbot)
    #     find_number = str(snapbot['players'][0]['steam_account'])
    #     print(find_number)
    #     check_for_number = re.compile(r'\d+')
    #     num_output = check_for_number.findall(find_number)
    #     print(num_output[0])
                    

def setup(bot):
    bot.add_cog(HeroCommand(bot))