import discord, os
from discord.ext import commands
from heroes import heroes

# def compare(self):
#     if self not in heroes:
#         print(f"{self} doesnt exist.")
#     else:
#         pass

def is_valid_hero(hero_name):
    return hero_name in heroes

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
    dotabuff_link = f"https://www.dotabuff.com/heroes/{dotabuff_hero_name}"
    dotawiki_link = f"https://dota2.gamepedia.com/{dotawiki_hero_name}"
    await ctx.send(f'Dotabuff: {dotabuff_link}\n DotaWiki: {dotawiki_link}')

if __name__ == '__main__':
    bot.run(os.environ.get("DISCORD_SECRET_KEY"))