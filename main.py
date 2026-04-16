import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import requests
from time import sleep as py_sleep # pls don't get confclited :pray:
from datetime import time, timezone, datetime

import oss
import analyze
from filterer import PhraseFilter

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('OSU_API_KEY')
database = "oss_stats.db"

hander = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="+", intents=intents)

f = PhraseFilter()
bad_words = []
with open("bad_words.txt", "r") as file: # this function gets line of words and allows to have each word splited up.
    for line in file:
        word = line.strip().lower().split()
        bad_words.append(word)
        f.add_phrase(word)

targets = [] # list for tracked users (REQ)
with open("targets.txt", "r") as file:
    for username in file:
        targets.append(username.strip())

@bot.event
async def on_ready():
    req.start() # startng daily function
    print(f"We are cute with {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if bot.user in message.mentions:
        if message.author.id == 1002359051092508792:
            await message.channel.send(f"Go away, {message.author.display_name}! (；¬д¬)")
        else:
            await message.channel.send(f"You thiniking of me >.<")
    
    if f.contains_banned(message.content):
        print(message.author, " tried to say ", message.content) 
        await message.delete()
        await message.channel.send(f"{message.author.mention}, don't use this word, you silly baka ! >:c")
    
    await bot.process_commands(message)

@bot.event
async def on_raw_message_edit(payload):
    msg = payload.message

    if msg is None:
        return  # not cached, fallback needed if you care # idk what my gpt is talking about here ngl.

    if msg.author == bot.user:
        return

    if f.contains_banned(msg.content):
        print(msg.author, " tried to say ", msg.content)
        await msg.delete()
        await msg.channel.send(f"{msg.author.mention}, don't use this word, you silly baka ! >:c")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def github(ctx):
    await ctx.send(f"Project: https://github.com/Pallid3/Thanatos")

CHANNEL_ID = 830453487015428147  # replace

@tasks.loop(time=time(hour=2, minute=0, tzinfo=timezone.utc))
async def req(): #requesting function
    print("Alustab REQ") # Starting REQ
    for username in targets:
        oss.make_user_request(username, API_KEY, database)
        a = analyze.compare_last_two_db(username, database)
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(f"{username} playcount increased by: {a}")
        print(f"{username} playcount increased by: {a}")
        py_sleep(2) # we sleep 2 seconds, cuz I doubt I can do many reqeuest at the time lol

@bot.command()
async def lasttwo(ctx, username: str = None):
    if not username:
        await ctx.send("Please provide a username! Example: `+lasttwo kellad`")
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

@bot.command()
async def playcount(ctx, *args):
    username = None
    day_start = None
    day_end = None

    # Case: at least 3 arguments -> maybe dates + username
    if len(args) >= 3:
        try:
            day_start = datetime.strptime(args[0], "%d.%m.%Y")
            day_end = datetime.strptime(args[1], "%d.%m.%Y")

            username = " ".join(args[2:])
        except ValueError:
            # If parsing fails, treat everything as username
            day_start = None
            day_end = None
            username = " ".join(args)

    # Case: no dates, only username
    else:
        username = " ".join(args)

    print("Start date:", day_start)
    print("End date:", day_end)
    print("Username:", username)



bot.run(token, log_handler=hander, log_level=logging.DEBUG)
