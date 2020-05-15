import discord, json, os
from discord.ext import commands

with open('heroes.json') as json_file:
    data = json.load(json_file)
    heroes = []
    for name in data['heroes']:
        #Take the common name of the hero from the dictionary and add to heroes list
        heroes.append((name['localized_name'].lower()))
    heroes.sort()

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')

@bot.command()
async def hero(ctx, *, arg):
    dotabuff_hero_name = arg.replace(" ", "-").lower()
    print(dotabuff_hero_name)
    dotawiki_hero_name = arg.replace(" ","_").title()
    print(dotawiki_hero_name)
    dotabuff_link = "https://www.dotabuff.com/heroes/"+dotabuff_hero_name
    dotawiki_link = "https://dota2.gamepedia.com/"+dotawiki_hero_name
    await ctx.send(f'Dotabuff: {dotabuff_link}\n DotaWiki: {dotawiki_link}')


bot.run(os.environ.get("DISCORD_SECRET_KEY"))