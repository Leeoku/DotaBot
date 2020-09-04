import discord
import requests
from discord.ext import commands


# .info [User_Id/Discord] shows general information about user
# .recent_games [User_Id] shows recent game info for user 
# .my_heros [User_Id] shows best heros, along with info for them, for selected user
# .my_items {uses/wins/kd/econ} best items for selected filter/user

#AFK A BIT WIL LEAVE THIS UP
# This is for any site we want to scrape. That would be a better option, I'll look at it too
def fetch(url):
    request = requests.get(url)
    if request.status_code == 200:
        return request
    raise ValueError(f"Site returned {request.status_code} instead of 200.")

class PlayerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # get username
    # 
    @commands.command()
    async def info(self, ctx, *, username):
        pass

def setup(bot):
    bot.add_cog(PlayerInfo(bot))
