import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import requests
from time import sleep as py_sleep # pls don't get confclited :pray:
from datetime import time, timezone

import oss
import analyze
from filterer import PhraseFilter

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('OSU_API_KEY')

database = "oss_stats.db"


f = PhraseFilter()
bad_words = []
with open("bad_words.txt", "r") as file: # this function gets line of words and allows to have each word splited up.
    for line in file:
        word = line.strip().lower().split()
        bad_words.append(word)
        f.add_phrase(word)

targets = []
with open("targets.txt", "r") as file:
    for username in file:
        targets.append(username)

hander = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    req.start()
    print(f"We are cute with {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if f.contains_banned(message.content):
        print(message.author, " tried to say ", message.content) 
        await message.delete()
        await message.channel.send(f"{message.author.mention}, don't use this word, you silly baka ! >:c")
    
    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    print(ctx)
    await ctx.send(f"Hello {ctx.author.mention}!")

CHANNEL_ID = 1200056673197371507  # replace

@tasks.loop(time=time(hour=2, minute=0, tzinfo=timezone.utc))
async def req():
    print("Alustab REQ")
    for username in targets:
        oss.make_user_request(username, API_KEY, andmebaas="oss_stats.db")
        a = analyze.compare_last_two_db(username, database)
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"{username} playcount increased by: {a}")
        print(f"{username} playcount increased by: {a}")
        py_sleep(2) # we sleep 2 seconds, cuz I doubt I can do many reqeuest at the time lol


@bot.command()
async def lasttwo(ctx, username: str = None):
    if not username:
        await ctx.send("Please provide a username! Example: `!lasttwo kellad`")
        return
    if not analyze.username_exists(username, database):
        await ctx.send(f"Username `{username}` not found in the database.")
        return
    try:
        diff = analyze.compare_last_two_db(username, database)
        await ctx.send(f"{username}'s playcount increased by: {diff}")
    except ValueError as e:
        print("Error code: 727 ", e, )
        await ctx.send("Error code: 727")

bot.run(token, log_handler=hander, log_level=logging.DEBUG)
