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
            'pos': 0,
            'top_5_heroes': [],
            'least_5_heroes':[],
        }
        await Doto().create(payload)
        print(f'{green} {steam_name} has been successfully entered into the data base{endc}')
        return

    # MONGODB VERSION
    @commands.has_permissions(administrator = True)
    @commands.command()
    async def deregister(self, ctx, *, steam_name=None):
        if steam_name is None:
            await ctx.send('Enter Steam name to deregister')
        #temp_admins = [382641335330537482, 122974788040785923 ]
        await Doto().delete(steam_name)
    @deregister.error
    async def deregister_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("This command is for admins only")

    # # JSON VERSION
    # @commands.command()
    # async def register(self, ctx, *, info=None):
    #     if info == None or len(info.split(",")) == 1:
    #         await ctx.send(f'<@{ctx.message.author.id}> Reenter as **!register Steam name, Dota name**.') 
    #         return
        
    #     dota_name = info.split(",")[0]
    #     steam_name = info.split(",")[1]

    #     with open('users.json', 'r') as f:
    #         json_data = json.load(f)
        
    #     if dota_name in json_data:
    #         await ctx.send(f"<@{ctx.message.author.id}> That account is already registered.")
    #         return
    #     else:
    #         json_data[dota_name] = {
    #             "Discord": ctx.author.id, 
    #             "Steam": steam_name, 
    #             "pos": 0, 
    #             "top_5_heroes": [],
    #             }

    #     with open('users.json', 'w') as f:
    #         f.write(json.dumps(json_data)) 

    #     await ctx.send("Registration complete")
    #     return
   
    # @commands.has_permissions(administrator = True)
    # @commands.command()
    # async def deregister(self, ctx, *, dota_name=None):
    #     #temp_admins = [382641335330537482, 122974788040785923 ]
        
    #     with open('users.json', 'r') as f:
    #         json_data = json.load(f)
    #     if dota_name == None:
    #         await ctx.send("Please enter a Dota username.")
    #         return 
    #     # elif ctx.author.id not in temp_admins:
    #     #     await ctx.send("This command is for admins only.")
    #     #     return
    #     elif dota_name not in json_data:
    #         print(json_data)
    #         await ctx.send("Enter correct Dota name")
    #         return
    #     json_data.pop(dota_name)
    #     await ctx.send(f"{dota_name} has been deregistered")
    #     with open('users.json', 'w') as f:
    #         f.write(json.dumps(json_data))
    #     return
    # @deregister.error
    # async def deregister_error(self, ctx, error):
    #     if isinstance(error, commands.MissingPermissions):
    #         await ctx.send("This command is  for admins only")

    # @commands.command()
    # async def register_discord(self, ctx, dota_name=None):
    #     if dota_name == None:
    #         await ctx.send(f"Enter your Dota name")
    #         return # You don't need else after return
        
    #     # Add the proper variables to this
    #     with open('users.json', 'r') as f:
    #         json_data = json.load(f)
        
    #     if dota_name in json_data: # keep this
    #         if json_data[dota_name]["Steam"]: # != None:
    #             # idk
    #             pass
    #         json_data[dota_name]["Steam"] = steam_name
    #     else:
    #         json_data[dota_name] = {"Discord": None, "Steam": steam_name}

    #     with open('users.json', 'w') as f:
    #         f.write(json.dumps(json_data))
        
    #     await ctx.send("Registered...")
    #     return

def setup(bot):
    bot.add_cog(Registration(bot))

# if steam_name is None:
#     await ctx.send('Enter your steam name')
#     return
# payload = {
#     '_id': ctx.author.id,
#     'steam_name':steam_name,
#     'pos': 0,
#     'top_5_heroes': [],
#     'least_5_heroes':[],
#     'profile_image': ''
# }
# await Doto().create(payload)
# print(f'{green} User has been successfully entered into the data base{endc}')
# return