# Dependancies
import discord_ios
import nextcord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Define the bot
activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=",help")
bot = commands.Bot(command_prefix=",", intents=nextcord.Intents.all(), activity=activity, help_command=None)

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