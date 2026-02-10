import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import requests
from datetime import time, timezone

import oss
import analyze

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('OSU_API_KEY')

with open("bad_words.txt", "r") as file:
    bad_words = [line.strip().lower() for line in file]

special_bad_words = []
with open("special_bad_words.txt", "r") as file: # this function gets line of words and allows to have each word splited up.
    for line in file:
        word = line.strip().lower().split()
        special_bad_words.append(word)

print(special_bad_words) # temp print

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

    if message.content.lower() in bad_words or message.content.lower() in special_bad_words:

        print(message.author, " tried to say ", message.content) 
        await message.delete()
        await message.channel.send(f"{message.author.mention}, don't use this word, you silly baka ! >:c")
    
    await bot.process_commands(message)

# sentence = message
# words = re.findall(r"\b\w+\b", sentence.lower())

# if "bananas" in words:
#     print("Found it!")
    # if message.content.lower() in bad_words or message.content.lower() in special_bad_words:


@bot.command()
async def hello(ctx):
    print(ctx)
    await ctx.send(f"Hello {ctx.author.mention}!")

CHANNEL_ID = 1200056673197371507  # replace

@tasks.loop(time=time(hour=2, minute=0, tzinfo=timezone.utc))
async def req():
    print("Alustab REQ")
    oss.make_user_request("kellad", API_KEY)
    entries = oss.read_data()
    a = analyze.compare_last_two()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"Data is: {entries[-1]}!")
        await channel.send(f"Playcount increased by: {a}")
    print(f"Data is: {entries[-1]}! owo")

@bot.command()
async def lastone(ctx):
    entries = oss.read_data()
    await ctx.send(f"Data is: {entries[-1]}!")

@bot.command()
async def lasttwo(ctx):
    a = analyze.compare_last_two()
    await ctx.send(f"Playcount increased by: {a}")


bot.run(token, log_handler=hander, log_level=logging.DEBUG)
