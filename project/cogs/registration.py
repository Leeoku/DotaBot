import discord
import json
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from helpers.colour import green, red, yellow, blue, purple, endc, bold, underline
from helpers import helpfunctions
from helpers.dbase import Doto

# .register v[Steam_Id] [Dota_Id] link steam id and user's discord
# .deregister [Steam/Discord] [Discord_Id] removes link between user and dota id

"""
File: users.json
User only added after calling .register or .steam_register
{
    "Dota_Id": {
        "Discord": None or Discord id
        "Steam": None or Steam id
    }
}
Add @task.loop to check if dota name changed
"""

class Registration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    #MONGO DB VERSION
    @commands.command()
    async def register(self, ctx, *, steam_name=None):
        if steam_name is None:
            await ctx.send('Enter your steam name')
            return
        payload = {
            '_id': ctx.author.id,
            'steam_name':steam_name,
            'top_5_heroes': [],
            'pos': 0
        }
        await Doto().create(payload)
        print(f'{green}{steam_name} has been successfully entered into the data base{endc}')
        await ctx.send(f'**{steam_name}** has been registered')
        return

    # MONGODB VERSION
    @commands.has_permissions(administrator = True)
    @commands.command()
    async def deregister(self, ctx, *, steam_name=None):
        print(steam_name)
        if steam_name is None:
            await ctx.send('Enter Steam name to deregister')
        #temp_admins = [382641335330537482, 122974788040785923 ]
        try:
            await Doto().delete(steam_name)
            await ctx.send(f'**{steam_name}** has been unregistered')
        except:
            pass
    @deregister.error
    async def deregister_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("This command is for admins only")

def setup(bot):
    bot.add_cog(Registration(bot))

