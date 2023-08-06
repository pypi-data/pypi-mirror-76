import os

import aiogram
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.environ["MONGO_URI"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
mongo_client = AsyncIOMotorClient(MONGO_URI)

BOT_TOKEN = os.environ["BOT_TOKEN"]
bot = aiogram.bot.Bot(BOT_TOKEN)
dp = aiogram.dispatcher.Dispatcher(bot, storage=MongoStorage(
    uri=MONGO_URI,
    db_name=DATABASE_NAME,
))
