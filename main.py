# Dependancies
import discord_ios
import nextcord
import asyncio
import os

# Imports
from nextcord.ext import commands
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")

# Set up the bot
activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{PREFIX}help")
bot = commands.Bot(command_prefix={PREFIX}, intents=nextcord.Intents.all(), activity=activity, help_command=None, shard_count=1)

# Load cogs
for fn in os.listdir("./cogs"):
    if fn.endswith(".py"):
        bot.load_extension(f"cogs.{fn[:-3]}")

# Events
@bot.event
async def on_ready():
    print("Bot is ready!")
    print(f"Logged in as {bot.user} ({bot.user.id})")
    print("-----------------------")

# Run the bot
bot.run(TOKEN)