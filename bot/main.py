import json
import discord
import os
from buzzsneakers.get_product import get_product as buzzsneakers_get_product
from buzzsneakers.embed import embed_builder as buzzsneakers_embed_builder

import datetime

import database.main as database
import utils as utils

intents = discord.Intents.default()
intents.message_content = True  

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

import dotenv
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

def run():
    bot.run(token)

if __name__ == "__main__":
    run()
