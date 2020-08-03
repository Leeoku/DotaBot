import discord
from discord.ext import commands, tasks
from datetime import datetime
from datetime import timedelta
from helpers.clearterm import fmtTime, cd, clearterm
from helpers.colour import purple, blue, green, red, bold, endc
import sys
import time as time
import traceback
from helpers.api_key import discord_key
import os
import aiohttp
import utils
import difflib 
import asyncio
import uvloop
from helpers import log
from discord.utils import find, get
from time import time
import logging



logger = log.get_logger(__name__)
command_logger = log.get_command_logger()


#Loading bar
def printProgressBar(iteration, total, prefix= '', suffix = '', decimals = 1, length = 100, fill = "█", printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    if iteration == total: 
        print(f'\r{purple}Loading Complete:             |{bar}| {percent}% {suffix}{endc}', end = printEnd)
    elif iteration in [0, 1]:
        print(f'\r{purple}{prefix} |{bar}| {percent}%   {suffix}{endc}', end = printEnd)
    else:
        print(f'\r{purple}{prefix} |{bar}| {percent}%  {suffix}{endc}', end = printEnd)


bot = commands.Bot(command_prefix = '!')
cogs = ['cogs.heroes', 'cogs.player_info', 'cogs.registration']
#Get closest command string
@bot.event
async def on_command_error(ctx, exception):
    if type(exception) == commands.CommandOnCooldown:
        await ctx.send("!{} is on cooldown for {:0.2f} seconds.".format(ctx.command, exception.retry_after))
    elif type(exception) == commands.CommandNotFound:
        cmd = ctx.message.content.split()[0][1:]
        try:
            closest = difflib.get_close_matches(cmd.lower(), list(bot.all_commands))[0]
        except IndexError:
            await ctx.send("!{} is not a known command.".format(cmd))
        else:
            await ctx.send("!{} is not a command, did you mean !{}?".format(cmd, closest))
    elif type(exception) == commands.CheckFailure:
        await ctx.send("You failed to meet a requirement for that ""command.")
    elif type(exception) == commands.MissingRequiredArgument:
        await ctx.send("You are missing a required argument for that ""command.")
    elif type(exception) == commands.BadArgument:
        await ctx.send("Invalid Argument.")
    else:
        pass
    print('Ignoring exception in command {}'.format(ctx.command),
          file=sys.stderr)
    traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr) 

#Loads the bot info
@bot.event
async def on_ready():
    # cache owner from appinfo
    bot.owner = (await bot.application_info()).owner
    bot.start_time = time()
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    logger.info("Loading complete")


@bot.before_invoke
async def before_any_command(ctx):
    ctx.timer = time()
    # try:
    #     await ctx.trigger_typing()
    # except discord.errors.Forbidden:
    #     pass


@bot.event
async def on_command_completion(ctx):
    # prevent double invocation for subcommands
    if ctx.invoked_subcommand is None:
        command_logger.info(log.log_command(ctx))



#Automatic bot reloading
@bot.command(name='reload',
             description='Reloads bot',
             aliases=['-r'],
             hidden=True,
             case_insensitive=True)
async def reload(ctx):
    """ Reloads cogs while bot is still online """
    user = ctx.author
    roles = ctx.message.author.roles
    server_id = ctx.guild.id
    updated_cogs = ''
    print(bot.loop)
    l = len(cogs)
    printProgressBar(0, l, prefix = 'Initializing:', suffix = 'Complete', length = 50)
    for i, cog in enumerate(cogs):
        printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
        bot.unload_extension(cog)
        bot.load_extension(cog)
        updated_cogs += f'{cog}\n'
    await ctx.send(f"`Cogs reloaded by:` <@{user.id}>")



# @bot.command()
# async def load(ctx, extension):
#     bot.load_extension(f'cogs.{extension}')

# @bot.command
# async def unload(ctx, extension):
#     bot.unload_extension(f'cogs.{extension}')

# for filename in os.listdir('./cogs'):
#     if filename.endswith('.py'):
#         bot.load_extension(f'cogs.{filename[:-3]}')

if __name__ == "__main__":
    for extension in cogs:
        try:
            bot.load_extension(f"{extension}")
            logger.info(f"Loaded [ {extension} ]")
        except Exception as error:
            logger.error(f"Error loading [ {extension} ]")
            traceback.print_exception(type(error), error, error.__traceback__)
    bot.run(discord_key, bot=True, reconnect=True)
    
'''
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
        await ctx.send(f"Please refine your search!")'''

