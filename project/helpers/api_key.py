import pymongo
import asyncio
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# discord_key = "YOUR DISCORD KEY HERE"
# cluster = AsyncIOMotorClient('YOUR MONGO CONNECTION HERE')


