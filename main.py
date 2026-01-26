import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import requests
from datetime import time

import oss

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('OSU_API_KEY')

hander = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"We are cute with {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, don't use this word, you silly baka ! >:c")
    
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    print(ctx)
    await ctx.send(f"Hello {ctx.author.mention}!")

@tasks.loop(time=time(2, 0))   # runs 5 or 4 am in estonia cba
async def req(ctx):
    print("Alustab REQ")
    oss.make_user_request("kellad", API_KEY)
    entries = oss.read_data()
    await ctx.send(f"Data is: {entries[-1]}!")
    print("Lõptab REQ")

@bot.command()
async def lastone(ctx):
    entries = oss.read_data()
    await ctx.send(f"Data is: {entries[-1]}!")

bot.run(token, log_handler=hander, log_level=logging.DEBUG)
