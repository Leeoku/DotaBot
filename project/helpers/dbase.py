from helpers.api_key import cluster
from datetime import datetime
import uvloop
import pymongo
import asyncio


db = cluster['leeoku']
dbs = {
    'dota':db.dota, 
    }

timestamp = datetime.utcnow()

class Doto:
    def by_id(self, id):
        self.id = id
        return self

    @property
    def monogo_dict(self):
        d = {}

        if hasattr(self, 'id'):
            d['_id'] = self.id

        return d

    async def get(self): 
        return await dbs['dota'].find_one(self.monogo_dict)

    async def push(self, _set):
        await dbs['dota'].update_one(self.monogo_dict, {'$push':_set})

    async def pull(self, _set):
        await dbs['dota'].update_one(self.monogo_dict, {'$pull':_set})

    async def update(self, _set):
        await dbs['dota'].update_one(self.monogo_dict, {'$set': _set})

    async def create(self, data):
        await dbs['dota'].insert_one(data)

    async def delete(self):
        await dbs['dota'].delete_one(self.monogo_dict)

    async def get_all(self):
        return await db['dota'].find().to_list(length=100000)

'''
Class().function(passtheID).function()
Doto().by_id(ctx.author.id).get()
ticket_collection.update({'_id':int(guild_id)}, {'$push':{'tickets':ticket_payload}})
'''


