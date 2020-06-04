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


    #SAMPLE HEADER
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