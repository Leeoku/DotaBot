import pymongo
import asyncio
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

discord_key = os.getenv("DISCORD_TOKEN")
mongo_connection = os.getenv("MONGO_URL")
cluster = AsyncIOMotorClient(mongo_connection)

