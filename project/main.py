import discord, os, operator
from discord.ext import commands
from heroes import heroes

def filter_hero(hero_name):
    filtered_heroes = []
    for e in heroes:
        if hero_name in e:
            filtered_heroes.append(e)
    if len(filtered_heroes) == 1:
        return filtered_heroes[0]
    elif len(filtered_heroes) == 0:
        return False
    else:
        return "multiple", filtered_heroes

def is_valid_hero(hero_name):
    #return (hero_name in heroes)
    if any(hero_name in s for s in heroes):
        return True
    else:
        return False

bot = commands.Bot(command_prefix = '!')

@bot.event
async def on_ready():
    print(f'{bot.user} is ready!')

@bot.command()
async def hero(ctx, *, arg=None):
    if arg != None:
        arg = arg.lower()
    else:
        pass
    if not arg:
        await ctx.send(f"Please enter hero!")    
    elif arg == None:
        await ctx.send(f"Hero doesn't exist!")  
    elif is_valid_hero(arg) == True and type(filter_hero(arg)) == tuple:
        print(filter_hero(arg))  
        print(filter_hero(arg)[1])
        await ctx.send(f'Please narrow your search for {filter_hero(arg)[1]}')
    elif is_valid_hero(arg) == True:      
        filter_hero_name = filter_hero(arg)
        dotabuff_hero_name = filter_hero_name.replace(" ", "-").lower()
        print(dotabuff_hero_name)
        dotawiki_hero_name = filter_hero_name.replace(" ","_").title()
        print(dotawiki_hero_name)
        dotabuff_link = f"https://www.dotabuff.com/heroes/{dotabuff_hero_name}"
        dotawiki_link = f"https://dota2.gamepedia.com/{dotawiki_hero_name}"
        await ctx.send(f'Dotabuff: {dotabuff_link}\n DotaWiki: {dotawiki_link}')
    else:
        #print(filtered)
        await ctx.send(f"Please refine your search!")

if __name__ == '__main__':
    bot.run(os.environ.get("DISCORD_SECRET_KEY"))